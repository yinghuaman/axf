$(document).ready(function(){
	var account = document.getElementById("account")
	var passwd = document.getElementById("psd")
	var passd = document.getElementById("confirmpsd")
	var email = document.getElementById("email")

	var accounterr = document.getElementById("accounterr")
	var checkerr = document.getElementById("checkerr")
	var passworderr = document.getElementById("passworderr")
	var confirmerr = document.getElementById("confirmerr")
	var emailerr = document.getElementById("emailerr")


	account.addEventListener("focus",function(){
		accounterr.style.display = "none"
		checkerr.style.display = "none"
	},false)

	account.addEventListener("blur",function(){
		var instr = this.value
		if(instr.length < 8 || instr.length > 20){
			accounterr.style.display = "block"
			return
		};
		$.post("/checkuserid/",{"userid":instr},function(data){
			if(data.status == "error"){
				checkerr.style.display = "block"
			}
		})
	},false)

	passwd.addEventListener("focus",function(){
	    passworderr.style.display = "none"
	},false)
	passwd.addEventListener("blur",function(){
	    var instr = this.value
	    if(instr.length <6 || instr.length >16){
	        passworderr.style.display = "block"
	    }
	},false)

	passd.addEventListener("focus",function(){
	    confirmerr.style.display = "none"
	},false)
	passd.addEventListener("blur",function(){
	    var instr = this.value
	    if(instr != passwd.value){
	        confirmerr.style.display = "block"
	    }
	},false)

	email.addEventListener("focus",function(){
	    emailerr.style.display = "none"
	},false)
	email.addEventListener("blur",function(){
	    instr = this.value
	    $.post("/checkemail/",{"email":instr},function(data){
			if(data.status == "error"){
				emailerr.style.display = "block"
			}
		})
	},false)
})