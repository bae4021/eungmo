# 내 도구 모음

## 주소 모음
- 응모 수첩: https://bae4021.github.io/eungmo/
- 연차관리대장: https://bae4021.github.io/eungmo/leave/
- Firebase 콘솔 (로그인·데이터·보안 규칙): https://console.firebase.google.com/project/eungmo
- 두 페이지 맨 위의 메뉴로 서로 오갈 수 있어요.

# 응모 수첩

출석체크, 이벤트 응모, 해지 기한을 관리하는 개인 수첩이에요.

- 주소: https://bae4021.github.io/eungmo/
- 기록은 Firebase(Firestore)에 저장되고, 보안 규칙으로 본인 구글 계정만 읽고 쓸 수 있어요.
- `fb.js`는 `tools/fb-entry.js`를 묶은 파일이에요 (firebase 12.19.0, esbuild).

## 연차관리대장

- 주소: https://bae4021.github.io/eungmo/leave/
- 기록은 Firestore `users/{uid}/apps/leave` 문서 하나에 저장돼요 (기존 아티팩트와 같은 구조).
- 같은 `fb.js`(저장소 맨 위)를 같이 써요.
