from flask import Flask, render_template, redirect, url_for, request


web_host = "192.168.0.107"
web_page = "https://google.com/"

app = Flask(__name__)


#웹 메인 페이지
@app.route('/', methods=['GET', 'POST'])
def main():
    #지도 정보를 가지고 있어야
    #get 같은걸로 맵을 가져와야하는거 같은데
    if request.method == 'POST':
        print("aa")
        return redirect(url_for('test'))
    return render_template('main.html')

@app.route('/test')
def show_map_page(robot_map):
    pass
    # cv2.imshow("RobotMap", robot_map)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

app.run(host=web_host, port=80, debug=True)
