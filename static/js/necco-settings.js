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
      	alert("成功しました");
      }
      else{
      	alert("情報更新に失敗しました");
      }
    }).fail(function(jqxhr, text, error){
      alert("失敗しました的なメッセージを表示しよう");
    });
  });
});
