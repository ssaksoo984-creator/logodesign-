# RED — Playbill

Triple M Productions · *Red* by John Logan
Dec 8–12, 2026 · 8 PM · The Nest, #101–1398 Cartwright St, Granville Island

판형 **5.5 × 8.5 in** + 도련 0.125 in → 재단 전 **5.75 × 8.75 in**, 12쪽.

---

## 1. 폴더 구조

```
playbill.html          ← 본체. 이 파일 하나만 고치면 됩니다. CSS가 <style>에 전부 들어 있어요.
img/                   ← playbill.html이 쓰는 이미지 27개
fonts/                 ← Pretendard, Instrument Serif, Inter, Source Serif
scripts/               ← PDF 만드는 스크립트
source/                ← 원본 자료 (편집용 원본, playbill.html은 안 씀)
  poster/              원본 포스터 고해상도
  headshots/           배우·스태프 사진 원본
  logos/               후원사 로고 원본
  reference/           처음 받은 레이아웃 더미 PDF
  ai-generated/        OpenArt로 만든 사진 4장 (스튜디오, 붓, 손, 페인트 캔)
  bios.md              받은 바이오 원문 (텍스트)
```

`playbill.html`을 브라우저에서 그냥 열면 펼침면 순서로 두 쪽씩 나란히 보여요.

---

## 2. 고치는 법

### 글자·색 바꾸기
`playbill.html` 맨 위 `<style>` 안에 있어요.

| 값 | 의미 |
|---|---|
| `#c8191e` | 레드 (포스터에서 뽑은 색) |
| `#333` | 본문 글자색 |
| `#ecebe7` | 종이색 |
| `#16191b` | 검정 페이지 |
| `Pt` | Pretendard — 본문·라벨 전부 |
| `Ds` | Instrument Serif — 큰 제목, 이름 |
| `Sn` | Inter — 아주 작은 대문자 라벨 |

### 주요 클래스

| 클래스 | 하는 일 |
|---|---|
| `.page` | 한 쪽. `.wht` `.red` `.blk` `.cov` 중 하나를 같이 붙여요 |
| `.body` | 본문 영역. 좌우 0.6in 여백 |
| `.rh` / `.rf` | 머리글 / 쪽번호 줄 |
| `.xl` | 아주 큰 제목 (2·3쪽) |
| `.th` | 보통 제목 + 빨간 네모 |
| `.lrow` `.idx` | `[01]` 번호가 붙은 목록 줄 |
| `.pill` | 테두리 알약 태그 |
| `.spd` | 양끝으로 벌린 작은 대문자 줄 |
| `.stmt` | 한 문장짜리 큰 글 |
| `.band` | 접힘선을 넘어가는 색 띠 |
| `.chip` | 노란 "아직 안 온 내용" 표시 — 최종본에서 전부 지우면 됩니다 |
| `.cap` | 작은 대문자 라벨 |
| `.acc` | 빨간 글자 |

### 쪽 구성

| 쪽 | 내용 | 바탕 |
|---|---|---|
| 1 | 표지 (원본 포스터) | 레드 |
| 2 | Cast & Creative — 번호 목록 | 종이 |
| 3 | Mark Rothko / The Play | 종이 + 레드 띠 |
| 4 | The Cast — Rob, Mozi 두 단 | 종이 |
| 5 | In Rehearsal | 레드 |
| 6 | Jennifer Copping (감독) | 종이 |
| 7 | Rhonda Dent (프로듀서) | 종이 |
| 8 | Design Team 3명 | 종이 |
| 9 | Production Team 3명 | 종이 |
| 10 | Thank You + 반 페이지 광고 | 종이 |
| 11 | Our Supporters | 종이 |
| 12 | 뒷표지 | 검정 |

6·7쪽은 사진이 가운데 접힘선에서 만나게 되어 있어서 **둘 중 하나만 바꾸면 어긋나요.** 같이 보세요.

---

## 3. PDF 만들기

```bash
pip install playwright pypdf pymupdf opencv-python-headless
playwright install chromium

python scripts/render.py  "$PWD/playbill.html"  out.pdf     # 12쪽 낱장
python scripts/outputs.py out.pdf  .                        # 인쇄소용(도련) + 교정용
python scripts/spreads.py out.pdf  spreads.pdf preview.jpg  # 펼침면
python scripts/booklet.py out.pdf  booklet.pdf              # 집에서 접어 만드는 2-up
python scripts/check.py   "$PWD/playbill.html"              # 글 넘침 검사 — []면 정상
```

`render.py`에 **절대경로**를 줘야 합니다. 상대경로면 Chromium이 못 찾아요.

인쇄소에는 `RED_Playbill_PRINT_bleed.pdf`를 보내세요. TrimBox/BleedBox가 들어 있어요.

### 이미지 다시 만들기
`scripts/assets6.py`가 `img/`의 빨간 듀오톤, 페인트 질감, 종이결, 그레인을 만들어요.
`source/ai-generated/`의 원본에서 출발합니다. 경로가 `build/img4`, `build/img6`로 되어 있으니 쓰시려면 고쳐야 해요.

`scripts/v11.py`는 지금 `playbill.html`을 만들어낸 생성기예요. 손으로 고치실 거면 안 쓰셔도 됩니다.

---

## 4. 아직 안 들어간 내용

노란 태그가 붙은 자리예요.

- [ ] Rob LaBelle 바이오 (4쪽) · 고해상도 사진
- [ ] Mozi Mayaleh 바이오 (4쪽) · 고해상도 사진
- [ ] 리허설 사진 (5쪽) — 지금은 임시 이미지
- [ ] 감사 명단 (10쪽)
- [ ] *Eureka Day* 광고 — 5.5 × 4.25 in + 도련 0.125 in, PDF 또는 300dpi JPG
- [ ] 뒷표지 연락처: 웹사이트, 인스타그램, 이메일
- [ ] Land acknowledgement 문안 확정
- [ ] 역할 확인: Sam Cheng(조명), Ben Elliott(음향), Elizabeth McCarthy Meek(홍보)
- [ ] 공연권 표기 줄 (보통 "Produced by special arrangement with …")

연출의 글은 뺀 상태예요. 다시 넣으시려면 5쪽 리허설 자리가 적당해요.

---

## 5. 알아두실 것

- **Rothko 사진**: 저작권 때문에 안 넣었어요. 넣으시려면 라이선스가 필요해요.
- **분홍 조심**: 레드 위에 흰색 반투명(`rgba(255,255,255,.4)` 같은)을 쓰면 분홍이 됩니다. 레드 페이지의 선은 `rgba(0,0,0,.14)`로 어둡게 깔았어요. 그레인도 레드 위에서는 `grain_soft.png`를 `multiply`로 써서 어두워지기만 해요.
- **Pretendard는 이탤릭이 없어요.** 본문에 `<i>`를 써도 안 기울어지게 꺼놨어요. 기울임은 제목(Instrument Serif)에서만 나와요.
- 쪽수는 **4의 배수**여야 중철 제본이 돼요. 지금 12쪽.

---

## 6. Figma로 옮기려면

`playbill.html`을 브라우저에서 열고 **html.to.design** 플러그인으로 가져오면 레이어가 살아서 들어와요.
PDF를 Illustrator로 열어도 되지만 텍스트가 깨질 수 있어요.
