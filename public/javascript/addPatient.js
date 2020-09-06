var btn = document.getElementById("create").addEventListener("click",function(){
	var patientId = ""+document.getElementById("PatientId").value;
	var gender = ""+document.getElementById("Gender").value;
	var age = ""+document.getElementById("Age").value;
	var authorized = ""+"[]";
	var patientObj = {
		"$class": "org.acme.biznet.Patient",
  		"PatientId": patientId,
  		"authorized": authorized,
  		"gender": gender,
  		"age": age
	}
	console.log(patientObj);
	var JSONobj = JSON.stringify(patientObj);
	$.ajax({
        type : 'POST', 
        url: 'http://localhost:3000/api/Patient',
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