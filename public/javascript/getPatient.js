var getRecord = document.getElementById("GetRecord").addEventListener("click",function(){
    var patientId = document.getElementById("patientId").value
    console.log(patientId)
    console.log("clicked");
    console.log(""+patientId+"??????"+localStorage.getItem('DoctorId'));
    $.ajax({
        type : 'GET',
        url: 'http://localhost:3000/api/queries/selectMedicalRecordByDoctorAndPatientId?DoctorId='+ localStorage.getItem('DoctorId') +'&PatientId='+patientId,
        dataType: 'json',
        async: false,
        success: function(response){
            console.log(response);
            localStorage.setItem("records",JSON.stringify(response));
            location.assign('http://localhost:4000/records.html');
        },
        error:function (request, status, error) {
            alert("Error");
        }
    });
})