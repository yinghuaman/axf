$(document).ready(function(){
    var alltypebtn = document.getElementById("alltypebtn")
    var showsortbtn = document.getElementById("showsortbtn")

    var typediv = document.getElementById("typediv")
    var sortdiv = document.getElementById("sortdiv")

    typediv.style.display = "none"
    sortdiv.style.display = "none"

    alltypebtn.addEventListener("click",function(){
        typediv.style.display = "block"
        sortdiv.style.display = "none"
    },false)

    showsortbtn.addEventListener("click",function(){
        typediv.style.display = "none"
        sortdiv.style.display = "block"
    },false)

    typediv.addEventListener("click",function(){
        typediv.style.display = "none"
    },false)

    sortdiv.addEventListener("click",function(){
        sortdiv.style.display = "none"
    },false)

    //修改购物车
    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")

    for (var i=0;i<addShoppings.length;i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click",function(){
            pid = this.getAttribute("ga")
            $.post("/changecart/0/",{"productid":pid},function(data){
                if(data.status == "success"){
                    //添加成功，将中间的innerHTML变成当前的数量

                    document.getElementById(pid).innerHTML = (data.data)[0]
                }
                else{
                    if(data.data == -1){
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }
                }
            })
        })
    }

    for (var i=0;i<subShoppings.length;i++){
        subShopping = subShoppings[i]
        subShopping.addEventListener("click",function(){
            pid = this.getAttribute("ga")
            $.post("/changecart/1/",{"productid":pid},function(data){
                if(data.status == "success"){
                    //减少一个，将中间的innerHTML变成当前的数量
                    if ((data.data)[0] == 0){
                        subShopping.style.display = "none"
                        document.getElementById(pid).innerHTML = ""
                    }
                    else{
                        subShopping.style.display = "inline-block"
                        document.getElementById(pid).innerHTML = (data.data)[0]
                    }
                }
                else{
                    if(data.data == -1){
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }
                }
            })
        })
    }

})