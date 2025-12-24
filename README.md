# LNK-Payload-Forge: APT Attack Replication Research



본 프로젝트는 **북한발 APT(Advanced Persistent Threat) 공격**에서 주로 발견되는 **LNK(바로가기) 파일 기반의 악성코드 유포 기법**을 연구하고 재현하기 위한 목적으로 제작되었습니다. 

특히 소만사(Somansa) 및 주요 보안 보고서에서 다뤄진 **Chinotto, RokRAT** 등의 공격 그룹이 사용하는 은닉 및 우회 기법을 파이썬 코드로 구현하여 보안 분석 역량을 강화하는 데 중점을 둡니다.

---

## 🚀 주요 기능 (Key Features)

* **Binary Overlay**: 정상 파일(PDF, Docx 등)의 바이너리 데이터를 LNK 파일 끝에 물리적으로 결합.
* **Self-Extraction**: LNK 실행 시 자기 자신의 바이너리 내에서 특정 **Hex Marker**를 탐색하여 페이로드를 자동 추출 및 실행.
* **Base64 Encoding**: PowerShell 페이로드를 UTF-16LE 기반 Base64로 인코딩하여 정적 탐지 우회.
* **Target Padding Bypass**: LNK 속성창의 길이 제한을 이용해 실제 명령어를 가리는 패딩 기법 적용.
* **Icon Spoofing**: 입력된 정상 파일의 확장자에 맞춰 시스템 아이콘을 자동으로 매칭.

---

## 🛠️ 설치 및 사용 방법

### 1. 필수 요구사항
* Python 3.x
* ```bash
    pip install pylnk3
    ```

### 2. 사용 단계
1.  프로젝트 디렉토리에 정상적인 미끼 파일(예: `report.pdf`)을 준비합니다.
2.  다음과 같이 실행합니다.
    ```bash
    python lnk_payload_forge.py
    ```
4.  안내에 따라 파일명, 추가 실행 명령어, 은닉 여부를 입력합니다.
5.  생성된 ```.lnk``` 파일을 통해 동작 및 보안 솔루션 탐지 여부를 분석합니다.

---

## 🔍 연구 분석 포인트 (Analysis)



본 도구는 다음과 같은 분석 관점을 제공합니다:

1.  **시그니처 기반 탐지**: 고유 Hex Marker 및 Base64 패턴이 최신 백신(AV) 및 EDR 솔루션에서 어떻게 식별되는지 분석.
2.  **행위 기반 분석**: PowerShell이 부모 프로세스 없이 실행되거나 임시 폴더(`%TEMP%`)에 파일을 생성하는 행위에 대한 로깅 모니터링.
3.  **포렌식 흔적**: 파일 실행 후 남는 Prefetch, LNK 파일의 속성 데이터, PowerShell 실행 이벤트 로그(Event ID 4104) 조사.

---

## ⚠️ 주의 사항 (Disclaimer)

* 본 프로그램은 오직 **교육 및 보안 연구(Ethical Hacking & Research)** 목적으로만 사용되어야 합니다.
* 승인되지 않은 시스템에서 본 도구를 실행하는 것은 불법이며, 모든 책임은 사용자에게 있습니다.
* 실제 환경에서의 테스트는 반드시 격리된 샌드박스(Sandbox) 환경에서 수행하십시오.

---

## 📝 관련 문서 및 참조
* Somansa: [LNK 악성코드 3종 분석 보고서]
* Microsoft: [Defending against PowerShell attacks]

---
**Developed for Security Research 2025**
