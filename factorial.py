from flask import Flask, render_template, request, jsonify

app = Flask(__name__,template_folder="templates") 

@app.route('/factorial',methods=['POST'])
def factorial():
    data=request.get_json()
    f=1
    print("Entered Number: ",data)

    for i in range(0,data):
        f=f*i
    
    print("factorial: ",f)
    return jsonify(f)


if __name__=='__main__':
    app.run(debug=True)



