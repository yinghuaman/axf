$(document).ready(function(){
    //修改购物车
    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")

    for (var i=0;i<addShoppings.length;i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click",function(){
            pid = this.getAttribute("ga")
            total = document.getElementById("totalprice").innerHTML
            $.post("/changecart/0/",{"productid":pid,"totalprice":total},function(data){
                if(data.status == "success"){
                    //添加成功，将中间的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = (data.data)[0]
                    document.getElementById(pid+"price").innerHTML = "￥"+(data.data)[1]
                    total = document.getElementById("totalprice");
                    total.innerHTML = data.totalprice;
                }

            })
        })
    }

    for (var i=0;i<subShoppings.length;i++){
        subShopping = subShoppings[i]
        subShopping.addEventListener("click",function(){
            pid = this.getAttribute("ga")
            total = document.getElementById("totalprice").innerHTML
            $.post("/changecart/1/",{"productid":pid,"totalprice":total},function(data){
                if(data.status == "success"){
                    //减少一个，将中间的innerHTML变成当前的数量
                    if((data.data)[0] == 0){
                        li = document.getElementById(pid+"li")
                        li.remove()
                    }
                    else{
                        document.getElementById(pid).innerHTML = (data.data)[0]
                        document.getElementById(pid+"price").innerHTML = "￥"+(data.data)[1]
                    }

                    total = document.getElementById("totalprice");
                    total.innerHTML = data.totalprice;
                }
            })
        })
    }

    var isChoses = document.getElementsByClassName("single-select")
    for (var i=0;i<isChoses.length;i++){
        isChose = isChoses[i]
        isChose.addEventListener("click",function(){
            pid = this.getAttribute("goodsid")
            total = document.getElementById("totalprice").innerHTML
            $.post("/changecart/2/",{"productid":pid,"totalprice":total},function(data){
                if(data.status == "success"){
                    var check = document.getElementById(pid+"a")
                    check.innerHTML = data.data
                    total = document.getElementById("totalprice")
                    total.innerHTML = data.totalprice
                }
            })
        })
    }

    var ok = document.getElementById("ok")
    ok.addEventListener("click",function()
    {
        var f = confirm("是否确认下单")
        if(f)
        {
            $.post("/saveorder/",function(data)
            {
                if(data.status == "success")
                {
                     windows.location.href = "http://127.0.0.1:8000/car/"
                }
            })
        }
    })
})