from playwright.sync_api import sync_playwright


def get_authorization_and_request():
    with sync_playwright() as p:
        # 启动浏览器并创建上下文
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 存储authorization的值
        authorization = None

        # 监听所有网络请求，提取authorization头
        def handle_request(request):
            nonlocal authorization
            headers = request.headers
            if 'authorization' in headers:
                authorization = headers['authorization']

        # 注册请求监听器
        page.on("request", handle_request)

        # 1. 访问页面，触发authorization生成
        page.goto("https://www.tjggzy.cn/announcementIndex")
        page.wait_for_load_state("networkidle")

        # 确保获取到authorization
        if not authorization:
            # 如果没捕获到，可以从context的cookies或localStorage中查找
            # 尝试从localStorage获取
            try:
                auth_storage = page.evaluate("() => localStorage.getItem('authorization')")
                if auth_storage:
                    authorization = auth_storage
            except:
                pass

        if not authorization:
            browser.close()
            return
        # 2. 使用提取的authorization发送POST请求
        try:
            response = context.request.post(
                url="https://www.tjggzy.cn/api/api/portal/Announcement/GetDetail",
                data={"Id": "1993623284155027456"},
                headers={
                    "Content-Type": "application/json",
                    "Referer": "https://www.tjggzy.cn/announcementIndex",
                    "Authorization": authorization,  # 关键：带上提取的authorization
                    "User-Agent": page.evaluate("navigator.userAgent")
                }
            )

            print("响应内容:", response.json())
            # {'responseData': {'announcementId': '1993623284155027456', 'announcementName': '武清开发区泉华路15号及泉明路10号厂房提升改造项目1标段施工招标公告', 'noticeContent': '<!DOCTYPE html><html> <head><meta charset="utf-8"> <title></title></head><body><div class="bodys mask"><div class="body" style="line-height: 30px;"><div id="RecordNumber"> 招标备案号：<span class="numeral" style="width: 150px;">JS1201142025114017</span></div><div> 招标项目编号：<span id="recordCodes" class="numeral" style="width: 138px;">I120000540500019B007</span></div><!----><!----><!----><div style="text-align: center; padding: 5px 0px;"><span class="title"> 施工招标公告 </span></div><div class="ct"><span id="spanGgbh" class="numeral underline" style="width: 150px; text-align: center;">  </span></div><div><div><div><div class="od"><strong>1、招标条件</strong></div></div><div><div colspan="2" style="padding-left: 30px;"><div><div class="ta-p-content"> 本招标项目<u>武清开发区泉华路15号及泉明路10号厂房提升改造项目</u><span> 已由天津市武清区行政审批局以津武审批投资备(2025)012号批准建设， 招标人为天津优达新智园区管理有限公司。建设资金为16000000元，资金来源为国内银行贷款11200000元，自筹及其他资金4800000元，资金来源已经落实。  </span><span> 建设规模为 <u>0平方米</u> 。 </span> 项目已具备招标条件， <!----><span><u>中瑞恒邦（天津）项目管理有限公司</u>受<u>天津优达新智园区管理有限公司</u>的委托，现对该项目的<u>施工</u>进行公开招标。 </span></div><!----></div></div></div><div><div class="od"><strong>2、项目概况与招标范围</strong></div><div style="padding-left: 30px;"><div><span class="pt">2.1 </span><span>项目概况：对泉华路15号、泉明路10号厂房进行屋面及消防提升改造，主要包括屋面、消防系统、设备、设施及管路提升改造工程，总改造建筑面积188187.56平方米，其中：最大单体建筑改造面积24000平方米，最高改造高度14.8米，最大改造单体跨度25米，具体内容详见招标人所发工程量清单。</span></div><div><span class="pt">2.2 </span><span>工程建设地点：武清开发区泉华路15号、泉明路10号</span></div><div><div class="pt" style="display: inline;">2.3</div><div style="display: inline;"> 标段划分与招标范围：共分 1 个标段。<br> 本次招标标段为：<br><!----><div> 一标段：标段名称：武清开发区泉华路15号仓库屋面防水工程施工 <span>招标范围:</span> 一是泉华路 15 号 A、B、C、D 四栋仓库屋面、天沟防水施工；二是泉旺路消防站拆除全部屋顶 GRC 檐口、外檐全面维修、局部屋面、女儿墙、雨蓬防水维修、幕墙窗户打胶、更换全部 PVC 雨水管、室外空调护栏除锈喷漆、更换自厨房至岗亭间配线及漏保等内容，总改造建筑面积80029.6平方米，其中：最大改造单体建筑面积24000平方米，最高改造高度14.8米，最大改造单体跨度25米，具体内容详见招标人所发工程量清单。本标段投资额约413.59万元。 </div><!----></div></div><div><div class="pt" style="display: inline;">2.4</div><div style="display: inline;"> 计划工期要求： <span> 2025年12月30日 至 2026年04月15日 </span></div></div><div><div class="pt" style="display: inline;">2.5</div><div style="display: inline;"> 工程质量要求：国家验收规范合格标准 </div></div></div></div><div><div class="od"><strong>3、投标人资格要求</strong></div><div style="padding-left: 30px;"><div><div class="pt" style="display: inline;">3.1</div><!----><div style="display: inline;"> 本次招标要求投标人具有： <div> 一标段: <br><span> 资质:</span><u></u><span>，资格:</span> <u>1、营业执照副本复印件并加盖公章，且在有效期内。2、具备建设行政主管部门颁发的防水防腐保温工程专业承包一级资质，资质证书副本复印件加盖公章且在有效期内。3、安全生产许可证在有效期内。4、项目部人员要求（1）正项目经理1名，应具有建设行政主管部门颁发的有投标资格的建筑工程一级注册建造师证书，具备5年及以上施工现场管理工作经历。（2）技术管理负责人1名，应具有工程技术类中级及以上职称，具备5年以上施工现场管理工作经历,需单独配备；（3）正项目经理和技术负责人均为本单位人员，应由投标企业任命并出具任命书；（4）项目部其他人员具体要求详见招标文件；5、为全面贯彻落实九部门联合印发了 《关于在招标投标活动中对失信被执行人实施联合惩戒的通知》（法〔2016〕285 号）和 《住房城乡建设部办公厅关于印发失信被执行人信用监督、警示和惩戒机制建设分工方案的通知》，本项目将在开标当日由招标代理单位在“信用中国”网站 （www.creditchina.gov.cn）打印投标单位的信用信息，并提交评标委员会，经评标委员会审核为失信被执行人的单位，取消投标资格</u><span>，本标段 <u>不接受</u> 联合体投标。</span></div></div><div><span class="pt" style="display: inline;">3.2</span><div style="display: inline;"> 各投标人均可对上述标段进行投标确认 <!----></div></div></div></div></div><div><div class="od" style="display: inline;"><strong>4、获取招标文件的时间和方式（北京时间）</strong></div><div style="display: inline;"><!----><div style="padding-left: 30px;"><div class="ta-p-maincontent"> 4.1招标文件的获取时间：2025年11月26日18时00分00秒至2025年12月03日18时00分00秒 </div><div class="ta-p-maincontent"> 4.2招标文件的获取方法：通过<u>天津市公共资源交易-投标服务平台 https://ebid.tjggzy.cn:8052</u>网址处获取电子招标文件 </div><!----></div></div></div></div><div><div class="od" style="display: inline;"><strong>5、投标文件的递交</strong></div><div style="padding-left: 30px;"><!----><div><div class="ta-p-maincontent"><span class="pt">5.1</span> 递交投标文件方式： <!----><span>网上递交</span></div><div class="ta-p-maincontent"><span class="pt">5.2 </span> 投标文件递交的截止时间为：<u>2025年12月17日09时30分00秒</u>，投标人应于当日<u>09时30分</u><!----><span>前将电子投标文件上传至<u>天津市公共资源交易-投标服务平台 https://ebid.tjggzy.cn:8052</u></span>。 </div></div></div></div><div><div class="od"><strong>6、定标方式</strong></div><div style="padding-left: 30px;"><div><div class="ta-p-maincontent"> 本项目是否采用评定分离方式：否。 </div></div></div></div><!----><!----><div style="padding: 20px 0px;"><strong>招标人：</strong><span class="numeral">天津优达新智园区管理有限公司</span><br><strong>法定代表人：</strong><span class="numeral">刘华中</span><br><strong>办公地址：</strong><span class="numeral">天津市武清开发区泉华路15号</span><br><strong>邮政编码：</strong><span class="numeral">301700</span><br><strong>联系人：</strong><span class="numeral">杜鹏</span><br><strong>电话：</strong><span class="numeral">022-82939816</span><br><strong>传真：</strong><span class="numeral">022-82939816</span><br><br><strong>招标代理机构：</strong><span class="numeral" style="width: 300px;">中瑞恒邦（天津）项目管理有限公司</span><br><strong>法定代表人：</strong><span class="numeral" style="width: 312px;">赵林旭</span><br><strong>办公地址：</strong><span class="numeral" style="width: 465px;">天津市武清区东蒲洼街道金侨大道商业街南东路423号（金瑞园底商423号）</span><br><strong>邮政编码：</strong><span class="numeral" style="width: 125px;">301700</span><br><strong>联系人：</strong><span class="numeral" style="width: 125px;">王工、慈工</span><br><strong>电话：</strong><span class="numeral" style="width: 125px;">022-82116815</span><br><strong>传真：</strong><span class="numeral" style="width: 125px;">022-82116815</span><div align="right"> 日期：2025年11月26日 </div></div><div style="font-weight: bold; padding-top: 20px; line-height: 28px;">违法违规举报：</div><div style="font-weight: bold; text-indent: 26px; line-height: 28px;"> 招标人或其招标代理机构应当对其提供的招标 公告 的真实性、准确性、合法性负责。 </div><div style="font-weight: bold; text-indent: 26px; line-height: 28px;"> 在招标投标活动中采取明招暗定、虚假招标、围标、陪标、串标和借照或挂靠等不正当手段获取工程的，将取消其中标资格，同时依据《中华人民共和国招标投标法》、《天津市建筑市场管理条例》等法律法规进行处理。 </div><div style="font-weight: bold; text-indent: 26px; line-height: 28px;"> 投标人在招标过程中如有异议请按照相关法律、法规的规定，向招标人提出质疑。对招标人答复仍持有异议的，向 天津市武清区建设工程招标服务站 实名投诉。 </div><div style="text-indent: 0px; margin-top: 25px; line-height: 28px;"><div style="font-weight: bold;">举报及投诉受理单位：</div><div style="margin-top: 12px;"><span class="numeral">天津优达新智园区管理有限公司</span><br> 受理负责人：<span class="numeral" style="width: 173px;">刘华中</span><br> 电话：<span class="numeral" style="width: 100px;">022-82939816</span><br> 传真：<span class="numeral" style="width: 100px;">022-82939816 </span><br> 受理单位地点：<span class="numeral" style="width: 591px;">天津市武清开发区泉华路15号</span><br></div><div style="margin-top: 12px;"><span class="numeral">  天津市武清区建设工程招标服务站 </span><br> 受理负责人：<span class="numeral" style="width: 173px;"> 刘晓熙 </span><br> 电话：<span class="numeral" style="width: 100px;"> 82190151 </span><br> 传真：<span class="numeral" style="width: 100px;"> 82190151 </span><br> 电子邮箱：<span class="numeral" style="width: 339px;"> wqqzjwzbz@tj.gov.cn </span><br> 受理单位地点：<span class="numeral" style="width: 591px;"> 天津市武清区市民服务中心602室 </span><br></div><div style="margin-top: 12px;"> 天津市公共资源交易网招投标投诉专区： http://ggzy.zwfwb.tj.gov.cn/ztbts/index.jhtml </div></div></div></div></div></body><style>.titleShow { display: none;}.title {font-size: 32px;text-align: center;line-height: 32px;}.body {padding: 30px;font-size: 14px;color: black;font-family: "微软雅黑"}.ct {text-align: center; padding: 5px 0px;}.od {vertical-align: top;padding-top: 0px;}.pt {width: 30px;vertical-align: top;margin-right: 8px;}.numeral {text-align: left;border: 0px;border-bottom: 1px solid black;line-height: 20px;}.body td {line-height: 26px;padding: 0 !important;}.underline {text-decoration: underline;}.body table {border: none !important;table-layout: fixed;line-height: 20px;}.body td {border: none !important;padding: 0 !important;}.body th {border: none !important;padding: 0 !important;}tbody > tr {background-color: #fff !important;}</style></html>', 'publishTime': '2025-11-26 18:00:00', 'publishingUnit': '天津市公共资源工程建设招投标平台', 'hits': 28, 'announcementCheckDetails': [{'stepName': '招标公告', 'announcementCheckChildDetailDtos': [{'id': '1993623284155027456', 'title': '武清开发区泉华路15号及泉明路10号厂房提升改造项目1标段施工招标公告', 'tenderProjectCode': 'I120000540500019B007', 'bidSectionCodes': 'I120000540500019B007001'}]}, {'stepName': '中标候选人公示', 'announcementCheckChildDetailDtos': []}, {'stepName': '中标结果公告', 'announcementCheckChildDetailDtos': []}], 'attachments': []}, 'statusCode': 2000, 'responseTime': '2025-11-26 23:38:03', 'responseMessage': '请求成功'}

        except Exception as e:
            print("请求失败:", str(e))

        browser.close()


if __name__ == "__main__":
    get_authorization_and_request()
