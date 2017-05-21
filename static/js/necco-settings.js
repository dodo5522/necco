$(function() {
  $("#buttonUpdateAccount").on("click", function() {
    var sending_data = $("#formAccount").serializeArray();
    $.ajax({
      type: "PUT",
      url: "/api/account",
      dataType: "json",
      data: sending_data
    }).done(function(data, text, jqxhr){
      if(text==="success"){
        swal({
          title:"　",
          text:"情報を更新しました",
          confirmButtonText: "了解！",
          type:"success"});
      }
      else{
        swal({
          title:"　",
          text:"情報を更新できませんでした",
          confirmButtonText: "しぶしぶ了解！",
          type:"error"});
      }
    }).fail(function(jqxhr, text, error){
      swal({
        title:"　",
        text:"情報を更新できませんでした",
        confirmButtonText: "しぶしぶ了解！",
        type:"error"});
    });
  });

  $("#buttonAddAbility").on("click", function(){
    swal("できること追加")
  });

  $("#buttonAddRequest").on("click", function(){
    swal("してほしいこと追加")
  });
});
