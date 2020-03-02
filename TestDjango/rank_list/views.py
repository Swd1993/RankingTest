import json

from django.http import JsonResponse

from django.views import View
from django_redis import get_redis_connection
# Create your views here.


class RankList(View):
    """"""

    @staticmethod
    def post(request):
        """
        上传分数
        :param request:
        :return:
        """
        args = json.loads(request.body)
        client_id = args.get("client_id")
        score = args.get("score")
        conn = get_redis_connection("default")
        conn.zadd(name="test:rank:list", mapping={client_id: score})
        rank = conn.zrevrank(name="test:rank:list", value=client_id) + 1
        return JsonResponse(
            {"msg": "数据更新成功", "data": {"client_id": client_id, "score": score, "rank": rank}, "code": 1}
        )


class RankQuery(View):
    """"""

    @staticmethod
    def get(request, client_id, start, end):
        """
        获取 名次段 内的成员
        :param request:
        :param client_id: 查询 ID
        :param start: 开始查询排名
        :param end: 结束查询排名
        :return:
        """
        conn = get_redis_connection("default")
        rank_list = conn.zrevrange(name="test:rank:list", start=start - 1, end=end - 1, withscores=True)
        print(rank_list)
        data = list()
        for i in range(1, len(rank_list) + 1):
            data.append(
                {
                    "rank": i,
                    "client_id": "".join(["客户端", bytes.decode(rank_list[i - 1][0])]),
                    "score": int(rank_list[i - 1][1])
                }
            )
        rank = conn.zrevrank(name="test:rank:list", value=client_id) + 1
        score = int(conn.zscore(name="test:rank:list", value=client_id))
        data.append({"rank": rank, "client_id": client_id, "score": score})
        return JsonResponse({"msg": "数据获取成功", "data": data, "code": 1})
