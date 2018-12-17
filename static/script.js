$(document).ready(function(){
$("#TODOform").submit(function(e){

    e.preventDefault();
    var form = $(this);

    $.ajax({
    type:"POST",
    url:"/add",
    datatype:"json",
    data :form.serialize(),
    success: function(data)
           {
               alert(data);
           }


    })
});

})
function edit_row(id){
  const elements = document.forms[0].elements;
  for (i=0; i<elements.length; i++){
    if (elements[i].name != ''){
      // console.log(elements[i].name);
    elements[i].value = document.getElementById(elements[i].name+'_'+id).innerText;
  }
  }
  toggle_form();

}
function toggle_form(flag){
      var form = document.getElementById("view-form");
      var data = document.getElementById("view-data");

        if (form.style.display === "none") {
        form.style.display = "block";
      } else {
        form.style.display = "none";
      }
      if (data.style.display === "none") {
      data.style.display = "block";
    } else {
      data.style.display = "none";
    }

    }
