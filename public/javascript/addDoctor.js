var btn = document.getElementById("create").addEventListener("click",function(){
	var doctorId = ""+document.getElementById("DoctorId").value;
	var doctorObj = {
		"$class": "org.acme.biznet.Doctor",
  		"DoctorId": doctorId,
	}
	console.log(doctorObj);
	var JSONobj = JSON.stringify(doctorObj);
	$.ajax({
        type : 'POST', 
        url: 'http://localhost:3000/api/Doctor',
        data : JSONobj,
        contentType: 'application/json',
        async: false,        
        success: function (response){
            console.log(response);
            if(response!=null){
                alert("done");
               location.assign('http://localhost:4000/admin.html')
            }
            else{
                alert("Error "); 		    		
            }
        },
        error: function (request, status, error) {
            alert("Error");
            console.log(error);
        }
    });
    return false;

})