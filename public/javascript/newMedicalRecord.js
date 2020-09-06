var button = document.getElementById("create").addEventListener("click",function(){
    console.log("clicked");
    var PatientId=""+document.getElementById("PatientId").value;
    var HospitalName =""+ document.getElementById("HospitalName").value;
    var Prescription =""+ document.getElementById("Prescription").value;
    var DoctorId=""+ localStorage.getItem("DoctorId");
    var RecordId =""+ Math.round(Math.random()*10000);
    var class1= "org.acme.biznet.UpdateRecord";
    var authorized = ""+"[]";
    var encounter_time = "2020-04-20T14:45:18.107Z";
    console.log(PatientId,HospitalName,Prescription,Date,DoctorId,RecordId);
    var RecordObject = {
        "$class" : class1, 
        "record_id" : RecordId,
        "PatientId": PatientId,
        "DoctorId": DoctorId,
        "authorized": authorized,
        "prescription": Prescription ,
        "description":Prescription,
        "encounter_time": encounter_time, 
        "version": "0",
        "location" : HospitalName       
    }
    console.log(JSONobj)
    var JSONobj = JSON.stringify(RecordObject);
    $.ajax({
        type : 'POST', 
        url: 'http://localhost:3000/api/UpdateRecord',
        data : JSONobj,
        contentType: 'application/json',
        async: false,        
        success: function (response){
            console.log(response);
            if(response!=null){
                alert("done");
               location.assign('http://localhost:4000/doctor.html')
            }
            else{
                alert("Ask the patient first to give you the write permission"); 		    		
            }
        },
        error: function (request, status, error) {
            alert("!!Ask the patient first to give you the write permission");
            console.log(error);
        }
    });
    return false;
})