import re
import ddddocr

from playwright.sync_api import sync_playwright, expect
from utils import generate_phone_number, username


def test_register_login():
    with sync_playwright() as p:
        # 配置浏览器启动选项，设置headless为False以显示浏览器界面
        browser = p.chromium.launch(headless=False, slow_mo=50, args=["--start-maximized"])  # slow_mo参数可控制执行速度，便于观察
        context = browser.new_context(no_viewport=True)
        page_register = context.new_page()
        # 数据
        # username = 'meiduo015'
        # cell_phone = '18866660007'
        pwd = 'meiduo001'
        # 注册
        page_register.goto("http://www.meiduo.site:8080")
        page_register.get_by_role("link", name="注册").click()
        page_register.locator("#user_name").fill(username)
        page_register.locator("#pwd").fill(pwd)
        page_register.locator("#cpwd").fill(pwd)
        page_register.locator("#phone").fill(generate_phone_number())
        ocr = ddddocr.DdddOcr(show_ad=False)
        captcha_img = page_register.get_by_role("img", name="图形验证码")
        # 2. 截图保存
        captcha_img.screenshot(path="captcha.png")
        image = open("captcha.png", "rb").read()
        result = ocr.classification(image)
        page_register.locator("#pic_code").fill(result)
        page_register.locator("#allow").click()
        page_register.get_by_role("button", name="注 册").click()
        page_register.wait_for_timeout(1000)
        # 登录
        page_register.get_by_role("link", name="登录").click()
        page_register.get_by_role("textbox", name="请输入用户名或手机号").fill(username)
        page_register.get_by_role("textbox", name="请输入密码").fill(pwd)
        page_register.get_by_role("checkbox").click()
        page_register.get_by_role("button", name="登 录").click()
        # get_by_text("欢迎您：meiduo001 退出")

        # 获取欢迎文本元素
        welcome_element = page_register.get_by_text(re.compile(r"欢迎您：.+ 退出"))

        # 方式1：使用 Playwright 断言元素文本
        expect(welcome_element).to_contain_text(f"欢迎您：{username} 退出")

        # # 使用正则表达式匹配包含"欢迎您："和用户名的文本
        # welcome_text = page_register.get_by_text(re.compile(r"欢迎您：.+ 退出")).text_content()
        # print(f'welcome_text:{welcome_text}')
        # print(f'welcome_text:{type(welcome_text)}')
        # # 提取用户名（假设格式为"欢迎您：用户名 退出"）
        # login_name = re.search(r"欢迎您：(.+?) 退出", welcome_text).group(1)
        # print(f"当前登录用户：{login_name}")
        # print(f"当前登录用户：{type(login_name)}")
        # print(f'data:{username}')
        # print(f'data:{type(username)}')
        # # 使用Playwright的expect断言
        # expect(login_name).to_contain_text(username)

        # 必须完全匹配（包括空格和标点）
        # expect(page.get_by_text("登录成功")).to_have_text("登录成功")
        page_register.pause()

        # 关闭浏览器
        browser.close()

# 运行测试函数
# test_has_title()
