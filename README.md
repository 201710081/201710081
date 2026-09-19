# SonMW

**Aspiring Data Analyst · milvus**

**데이터가 만들어지는 과정부터 이해하고, 신뢰할 수 있는 분석으로 연결하는 데이터 분석가를 지향합니다.**

밀버스 소속 대리로, 고객사 **ADAPT(어댑트)** 프로젝트의 데이터 플랫폼 업무를 인수해 운영·개선하고 있습니다.
여러 커머스 채널에서 수집한 데이터를 공통 기준으로 정리하고, Salesforce Data Cloud와 Tableau Next에서 활용할 수 있는 분석용 데이터로 연결하는 업무를 맡고 있습니다.

현재의 데이터 수집·모델링·검증 경험을 바탕으로, 지표의 변화를 설명하고 비즈니스 의사결정에 도움이 되는 분석까지 역할을 넓혀가고자 합니다.

<br/>

<h2>💼 경력 · 활동</h2>

<table>
<tr><th width="150">기간</th><th width="210">소속</th><th width="550">역할 · 내용</th></tr>
<tr>
<td valign="top"><code>2026.08 초 ~ 현재</code></td>
<td valign="top"><b>milvus · 밀버스</b><br/>데이터 컨설팅·구축 기업</td>
<td>
<b>대리</b>
<ul>
  <li>
    <b>ADAPT 프로젝트</b> · 고객사: 어댑트<br/>
    커머스 데이터 플랫폼 업무 인수 및 운영·개선
    <ul>
      <li>멀티 채널 커머스 데이터 수집부터 분석용 데이터 제공까지 운영</li>
      <li>Amazon Athena · dbt 기반 공통 데이터 모델 관리 및 개선</li>
      <li>매출·광고 데이터의 집계 기준 확인 및 정합성 검증</li>
      <li>Salesforce Data Cloud 연동 · Tableau Next 데이터 원본 관리</li>
      <li>데이터 처리 오류 원인 분석, 재처리 및 운영 문서 정리</li>
    </ul>
  </li>
</ul>
</td>
</tr>
</table>

<br/>

<h2>📊 ADAPT 프로젝트 · 담당 업무</h2>

여러 판매 채널의 데이터를 통합해 커머스 매출과 광고 지표를 분석할 수 있도록 지원하는 프로젝트입니다.
기존 데이터 플랫폼과 관련 업무를 인수받아, 데이터 흐름과 업무 규칙을 파악하고 운영·유지보수와 개선을 담당하고 있습니다.

### 1. 커머스 데이터 수집 및 ELT 파이프라인 운영

- 채널별 API와 원천 데이터 구조를 파악하고, AWS Lambda 기반 데이터 수집·적재 흐름을 관리합니다.
- Amazon S3에 적재된 원천 데이터가 Athena와 후속 변환 단계에서 정상적으로 조회되는지 확인합니다.
- 수집 누락, 중복 적재, 데이터 갱신 지연이 발생하면 처리 단계별로 원인을 추적하고 재처리 범위를 확인합니다.
- 데이터 수집 이후의 모델 변환과 분석 플랫폼 반영까지 이어지는 흐름을 점검합니다.

### 2. 공통 데이터 모델 및 집계 기준 관리

- 채널마다 다른 주문·결제·취소·반품 데이터 구조를 공통 기준으로 다룰 수 있도록 dbt 모델과 Athena VIEW를 관리합니다.
- 원천 필드의 의미와 변환 로직을 확인하고, 조인 키와 데이터 단위가 분석 목적에 맞게 연결되는지 점검합니다.
- 매출·광고 데이터를 집계할 때 적용되는 날짜, 상태, 분류 기준을 확인해 지표 차이가 발생하는 지점을 살펴봅니다.
- 모델 수정 시 후속 집계와 분석용 데이터에 미치는 영향을 확인하고, 변경 전후 결과를 비교합니다.

### 3. 데이터 정합성 검증 및 차이 원인 분석

- 원천 데이터, 변환 모델, 최종 집계 결과를 단계별로 비교해 숫자가 달라지는 구간을 확인합니다.
- SQL을 활용해 행 수, 키 중복, 누락값, 조인 결과와 주요 금액 합계를 검증합니다.
- 전체 합계뿐 아니라 기간·채널 등 세부 단위로 데이터를 나눠 차이의 원인을 추적합니다.
- 데이터 자체의 문제와 집계·변환 로직의 문제를 구분하고, 수정 후 동일한 기준으로 다시 검증합니다.

### 4. Salesforce Data Cloud 연동 및 BI 데이터 지원

- Salesforce Data Cloud로 이어지는 적재·매핑·갱신 흐름을 관리합니다.
- 변환된 데이터가 분석 플랫폼에 반영되었는지 확인하고, 데이터 모델과 집계 결과의 연결 관계를 점검합니다.
- Tableau Next에서 활용하는 분석용 데이터 원본을 관리하고, 조회에 필요한 데이터 구조를 확인합니다.
- BI에서 보이는 수치에 대한 확인이 필요하면 원천 데이터와 변환·집계 과정을 거슬러 올라가 근거를 찾습니다.

### 5. 운영 이슈 대응 및 업무 문서화

- 인수받은 시스템의 구성, 데이터 흐름과 운영 절차를 파악하고 실제 처리 상태와 대조합니다.
- 오류가 발생하면 수집·변환·적재·집계 중 어느 단계의 문제인지 구분해 대응합니다.
- 수정 사항은 기존 결과와의 비교 및 재검증을 거쳐 확인하고, 후속 처리에 미치는 영향을 점검합니다.
- 반복적으로 확인해야 하는 검증 항목과 이슈 대응 과정을 정리해 이후 운영에 활용합니다.

<br/>

<h2>🎯 데이터 분석가로서의 방향</h2>

현재 담당하는 데이터 플랫폼 업무를 분석의 기반으로 삼아, 다음 영역으로 역량을 확장하고자 합니다.

| 방향 | 지향하는 분석 |
| --- | --- |
| **비즈니스 질문과 지표 정의** | 무엇을 알고 싶은지 먼저 정리하고, 질문에 맞는 지표·집계 단위·비교 기준을 설정하는 분석 |
| **커머스 성과 분석** | 매출과 주문의 변화를 기간·채널별로 나눠 살펴보고, 변화의 원인을 설명하는 분석 |
| **마케팅 성과 해석** | 광고 데이터와 매출 데이터의 기준을 이해하고, 비교 가능한 범위에서 성과를 해석하는 분석 |
| **시각화와 커뮤니케이션** | 결과와 함께 지표의 정의, 해석의 근거와 한계를 전달해 의사결정에 도움이 되는 분석 |

<br/>

<h2>🛠 Tech Stack</h2>

<table>
<tr>
<td width="180"><b>Languages</b></td>
<td><img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white"/> <img alt="SQL" src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&amp;logoColor=white"/></td>
</tr>
<tr>
<td><b>Cloud &amp; Data Engineering</b></td>
<td><img alt="AWS Lambda" src="https://img.shields.io/badge/AWS%20Lambda-FF9900?style=flat-square&amp;logoColor=white"/> <img alt="Amazon S3" src="https://img.shields.io/badge/Amazon%20S3-569A31?style=flat-square&amp;logoColor=white"/> <img alt="Amazon Athena" src="https://img.shields.io/badge/Amazon%20Athena-8C4FFF?style=flat-square&amp;logoColor=white"/> <img alt="dbt" src="https://img.shields.io/badge/dbt-FF694B?style=flat-square&amp;logo=dbt&amp;logoColor=white"/></td>
</tr>
<tr>
<td><b>Data Platform &amp; BI</b></td>
<td><img alt="Salesforce Data Cloud" src="https://img.shields.io/badge/Salesforce%20Data%20Cloud-00A1E0?style=flat-square&amp;logoColor=white"/> <img alt="Tableau Next" src="https://img.shields.io/badge/Tableau%20Next-E97627?style=flat-square&amp;logoColor=white"/></td>
</tr>
</table>

### 업무에서의 활용

| 기술 | 활용 영역 |
| --- | --- |
| **SQL · Amazon Athena** | 원천 데이터 탐색, 조인·집계 로직 확인, 데이터 대사 및 차이 원인 분석 |
| **Python** | 데이터 처리, 반복 검증과 운영 작업 자동화 |
| **dbt** | 채널별 데이터를 공통 구조로 변환하는 모델 관리 및 수정 |
| **AWS Lambda · Amazon S3** | API 데이터 수집, 원천 적재 및 후속 처리 흐름 운영 |
| **Salesforce Data Cloud** | 데이터 연동·매핑·갱신과 분석용 집계 데이터 관리 |
| **Tableau Next** | BI 분석에 필요한 데이터 원본 관리 및 수치 확인 지원 |
