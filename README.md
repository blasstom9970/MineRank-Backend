좋습니다. 서버 API에 어떤 엔드포인트가 필요하고 Vite에서 어떤 설정을 해야 하는지 간단히 정리합니다.

핵심 엔드포인트 (권장)
- GET /api/users
  - 설명: 사용자 목록
- GET /api/servers
  - 설명: 서버 목록 (쿼리: page, limit, q, sort 등)
- GET /api/reviews
  - 설명: 리뷰 목록 (쿼리: serverId, page, limit)
- GET /api/gallery
  - 설명: 갤러리 게시물 목록
- GET /api/community/posts
  - 설명: 커뮤니티 게시물 목록 (쿼리: page, limit, q)
- GET /api/community/posts/:id
  - 설명: 커뮤니티 게시물 상세
- GET /api/community/comments
  - 설명: 댓글 목록 (쿼리: postId, page, limit)

- POST /api/servers
  - 설명: 서버 등록 (요청 본문: name, ip, version, description, tags[], maxPlayers, bannerUrl)
  - 응답: 201 + 생성된 Server 객체 (id, rank, onlinePlayers 포함)
- POST /api/reviews
  - 설명: 리뷰 생성 (요청 본문: serverId, userId, rating, content)
  - 응답: 201 + 생성된 Review
- POST /api/community/posts
  - 설명: 게시물 생성 (요청 본문: title, content, authorId, tags[])
  - 응답: 201 + 생성된 CommunityPost
- POST /api/community/comments
  - 설명: 댓글 생성 (요청 본문: postId, authorId, content)
  - 응답: 201 + 생성된 CommunityComment

권장 응답/오류 형식
- 성공: 200 / 201과 JSON(목록은 배열, 단건은 객체)
- 오류: 적절한 상태 코드와 JSON { error: string } 또는 { message: string }
- 입력 검증 실패: 400, 인증 필요: 401, 권한 부족: 403, 서버 오류: 500

TODO List
- [X] CORS 설정(클라이언트 도메인 허용)
- [ ] 비밀번호 Flask bcrypt 해시 암호화 
- [ ] 속도 제한(rate limiting) 할지 안 할지 모름
- [ ] login/signup/logout
- [ ] Endpoint들 구현
- [ ] DB 연동 (Duck DB)
- [ ] File Storage 폴더 생성 및 연결