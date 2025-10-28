from db_manager import DataBaseManager
import duckdb
import sqlite3 # DB Base

conn = duckdb.connect('minerank.db')
DB = DataBaseManager(cursor=conn.cursor())

#review_list = [
#    { "serverId": 1, "user": 1, "rating": 5, "comment": '역대 최고의 서버! 커뮤니티가 훌륭하고 미니게임이 정말 재미있어요.', "timestamp": '2023-10-26T10:00:00Z' },
#    { "serverId": 1, "user": 1, "rating": 4, "comment": '정말 멋진 생존 경험. 다만 피크 시간대에는 가끔 렉이 걸려요.', "timestamp": '2023-10-25T18:30:00Z' },
#    { "serverId": 2, "user": 1, "rating": 5, "comment": '건축가들에게 완벽한 곳. 스태프들이 매우 친절하고 부지가 엄청 넓어요.', "timestamp": '2023-10-26T11:00:00Z' },
#    { "serverId": 3, "user": 1, "rating": 4, "comment": '퀘스트가 정말 잘 짜여 있어요. 엔드게임 콘텐츠가 더 많았으면 좋겠어요.', "timestamp": '2023-10-24T14:00:00Z' },
#]

#DB.init_db('review', '''
#    "serverId" INTEGER,
#    "user" INTEGER,
#    "rating" INTEGER,
#    "comment" TEXT,
#    "timestamp" TEXT
#''')

#for i in review_list:
#    DB.add_entry("review", i)

server_list = [
    {
        "rank": 3,
        "name": '픽셀버스',
        "ip": 'play.pixelverse.net',
        "version": '1.20.1',
        "description": '궁극의 생존 및 미니게임 경험. 주간 이벤트와 커스텀 플러그인이 있는 커뮤니티에 참여하세요.',
        "tags": ['생존', '미니게임', '경제', 'PvP'],
        "maxPlayers": 2000,
        "bannerUrl": 'https://picsum.photos/seed/pixelverse/1200/300',
    },
    {
        "rank": 2,
        "name": '블록키크래프트',
        "ip": 'mc.blockycraft.com',
        "version": '1.19.4',
        "description": '창의적인 건축과 평화로운 생존에 초점을 맞춘 친근한 커뮤니티 중심 서버입니다.',
        "tags": ['건축', '생존', '커뮤니티', '가족친화적'],
        "maxPlayers": 1000,
        "bannerUrl": 'https://picsum.photos/seed/blockycraft/1200/300',
    },
    {
        "rank": 1,
        "name": '에테리아 렐름',
        "ip": 'join.aetheriarealms.io',
        "version": '1.20.1',
        "description": 'RPG 서버에서 독특한 퀘스트, 던전, 장대한 스토리라인이 있는 광대한 커스텀 세계를 탐험하세요.',
        "tags": ['RPG', '어드벤처', '퀘스트', '판타지'],
        "maxPlayers": 1000,
        "bannerUrl": 'https://picsum.photos/seed/aetheria/1200/300',
    },
    {
        "rank": 4,
        "name": '크래프트 앤 컨커',
        "ip": 'cnc.server.gg',
        "version": '1.18.2',
        "description": '제국을 건설하고 경쟁을 지배하는 하드코어 팩션 서버. 강렬한 PvP 액션을 즐겨보세요.',
        "tags": ['팩션', 'PvP', '하드코어', '레이드'],
        "maxPlayers": 500,
        "bannerUrl": 'https://picsum.photos/seed/conquer/1200/300',
    },
]

for server in server_list:
    DB.add_entry("servers",{
        "ip": server["ip"],
        "name": server["name"],
        "version": server["version"],
        "description": server["description"],
        "tags": ','.join(server["tags"]),
        "maxPlayers": server["maxPlayers"],
        "bannerUrl": server["bannerUrl"],
        "rank": server["rank"],
    })

"""cursor.execute(f'''
CREATE TABLE servers (
    "ip" TEXT PRIMARY KEY,
    "name" TEXT,
    "version" TEXT,
    "description" TEXT,
    "tags" TEXT,
    "maxPlayers" INTEGER,
    "bannerUrl" TEXT,
    "rank" INTEGER
);''')
"""
gallery = [
    { "id": 1, "serverId": 1, "user": 1, "imageUrl": 'https://picsum.photos/seed/gallery1/600/400', "caption": '새로운 성 건축!', "timestamp": '2023-10-25T12:00:00Z' },
    { "id": 2, "serverId": 1, "user": 1, "imageUrl": 'https://picsum.photos/seed/gallery2/600/400', "caption": '스플리프 토너먼트에서 우승했어요!', "timestamp": '2023-10-24T20:00:00Z' },
    { "id": 3, "serverId": 1, "user": 1, "imageUrl": 'https://picsum.photos/seed/gallery3/600/400', "caption": '스폰에서 찍은 단체 사진.', "timestamp": '2023-10-23T15:45:00Z' },
    { "id": 4, "serverId": 2, "user": 1, "imageUrl": 'https://picsum.photos/seed/gallery4/600/400', "caption": '내 건축 부지가 점점 멋져지고 있어요.', "timestamp": '2023-10-26T09:00:00Z' },
    { "id": 5, "serverId": 3, "user": 1, "imageUrl": 'https://picsum.photos/seed/gallery5/600/400', "caption": '멋진 던전을 발견했어요!', "timestamp": '2023-10-22T22:10:00Z' },
]

for i in gallery:
    DB.add_entry("gallery", i)

#DB.init_db('gallery', '''
#    "id" TEXT PRIMARY KEY,
#    "serverId" INTEGER,
#    "user" INTEGER,
#    "imageUrl" TEXT,
#    "caption" TEXT,
#    "timestamp" TEXT
#''')