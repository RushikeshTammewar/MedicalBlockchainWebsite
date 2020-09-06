var gender,age;
function patientdetails(patientId){
  console.log(patientId);
  $.ajax({
      type : 'GET',
      url: 'http://localhost:3000/api/Patient/'+patientId,
      dataType: 'json',
      async: false,
      
      success: function (response){
        gender=response.gender;
        age=response.age;
        console.log(gender)
        console.log(age)     
      },
      error: function (request, status, error) {
      alert("Error");
      console.log(error);
      }
  });
}

function displayRecords(){
    var response = JSON.parse(localStorage.getItem("records"));
    var table = document.getElementById("myTable");
    for(var i=0;i<response.length;i++){
       var row=table.insertRow(-1);
       var cell0=row.insertCell(0);
       var cell1=row.insertCell(1);
       var cell2=row.insertCell(2);
       var cell3=row.insertCell(3);
       var cell4=row.insertCell(4);
       var cell5=row.insertCell(5);
       var cell6=row.insertCell(6);
       var cell7=row.insertCell(7);
       var cell8=row.insertCell(8);
       patientdetails(response[i].PatientId);
       cell0.innerHTML = response[i].record_id;
       cell1.innerHTML = response[i].PatientId;
       cell2.innerHTML = response[i].DoctorId;
       cell3.innerHTML = gender;
       cell4.innerHTML = age;
       cell5.innerHTML = response[i].prescription;
       cell6.innerHTML = response[i].description;
       cell7.innerHTML = response[i].encounter_time;
       cell8.innerHTML = response[i].location;

    }
    console.log(response);
}

