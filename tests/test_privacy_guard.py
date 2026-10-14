import importlib.util
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'privacy_guard.py'

class PublicationGuardTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.exists(), 'Publication guard must exist before publishing')
        spec = importlib.util.spec_from_file_location('guard', SCRIPT)
        self.guard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.guard)

    def test_data_and_disguised_data_are_blocked(self):
        for name, body in [('data.csv', b'a,b\n1,2'), ('docs/report.xlsx', b'PK'),
                           ('docs/report.md', b'PK\x03\x04data'), ('docs/report.md', b'a\x00b'),
                           ('docs/customer.json', b'{}'), ('docs/report.twb', b'<workbook/>'),
                           ('docs/raw/report.md', b'private')]:
            with self.subTest(name=name):
                self.assertTrue(self.guard.check_blob(name, body))

    def test_business_numbers_are_blocked_without_echoing_values(self):
        for s in ['매출 123,456원', '환불 42건', '성장률 35.7%', '매출 １２３원',
                  '| 거래처 | 12345 |', '달성률 백 퍼센트', '<!-- 매출 500 -->']:
            with self.subTest(s=s):
                errors = self.guard.check_blob('docs/story.md', s.encode())
                self.assertTrue(errors)
                self.assertNotIn(s, str(errors))

    def test_masked_prose_dates_headings_and_technical_names_are_allowed(self):
        text = '# ADAPT\n## 1. 수행 내용\n# 02 · 화면\n2026.08.25 ~ 현재\n2026-10-14 기준\nS3 · B2B · Cafe24 · Qoo10\nS3에 저장\n매출 [마스킹], 처리량 [마스킹]\n'
        self.assertEqual([], self.guard.check_blob('docs/story.md', text.encode()))

    def test_credentials_contacts_and_internal_links_are_blocked(self):
        for s in ['person@example.com', '010-1234-5678', 's3://private-bucket/path',
                  'https://tenant.my.salesforce.com/path', 'C:\\Users\\person\\data',
                  'ghp_' + 'A' * 36, 'password = "example-value"']:
            with self.subTest(s=s):
                self.assertTrue(self.guard.check_blob('docs/story.md', s.encode()))

    def test_new_binary_and_symlink_are_blocked(self):
        self.assertTrue(self.guard.check_blob('docs/new.png', b'\x89PNG\r\n'))
        self.assertTrue(self.guard.check_blob('docs/link.md', b'target', mode='120000'))

    def test_staged_blob_is_checked_even_when_worktree_is_masked(self):
        with tempfile.TemporaryDirectory() as d:
            def git(*args):
                return subprocess.run(['git', '-C', d, *args], check=True, capture_output=True)
            git('init', '-q')
            f = pathlib.Path(d)/'README.md'
            f.write_text('매출 654321원', encoding='utf-8')
            git('add', 'README.md')
            f.write_text('매출 [마스킹]', encoding='utf-8')
            self.assertTrue(self.guard.check_snapshot('INDEX', cwd=d))
            git('add', 'README.md')
            self.assertEqual([], self.guard.check_snapshot('INDEX', cwd=d))

    def test_intermediate_commit_is_checked_even_after_data_is_deleted(self):
        with tempfile.TemporaryDirectory() as d:
            def git(*args):
                return subprocess.run(['git', '-C', d, *args], check=True, capture_output=True).stdout.decode().strip()
            git('init', '-q'); git('config', 'user.name', 'Test'); git('config', 'user.email', 'test@example.invalid')
            f = pathlib.Path(d)/'README.md'; f.write_text('safe')
            git('add', '.'); git('commit', '-qm', 'base'); base = git('rev-parse', 'HEAD')
            data = pathlib.Path(d)/'data.csv'; data.write_text('x\n1')
            git('add', '.'); git('commit', '-qm', 'data')
            git('rm', '-q', 'data.csv'); git('commit', '-qm', 'remove')
            self.assertTrue(self.guard.check_range(base, 'HEAD', cwd=d))

if __name__ == '__main__':
    unittest.main()
