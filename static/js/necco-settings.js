$(function() {
  $("#navbarItemSettings").on("click", function() {
    hideContent();
    activateNavbarItem("#navbarItemSettings");

    $.ajax({
      type: "GET",
      url: "/api/account",
      dataType: "json"
    }).done(function(data, text, jqxhr){
      for(var key in data){
        $("#" + key).val(data[key]);
      }
      showContent("#contentSettings");
    }).fail(function(jqxhr, text, error){
      showContent("#contentSettings");
    });

    $.ajax({
      type: "GET",
      url: "/api/abilities/0", // myself
      dataType: "json",
    }).done(function(data, text, jqxhr){
      var ulAbility = $("#listAbility");
      ulAbility.empty();
      for(var i = 0; i < data.length; i++){
        var liAbility = $("<li>");
        liAbility.text(data.body[i].detail);
        liAbility.attr("id", "itemsListAbility" + i);
        liAbility.addClass("itemsListAbility");
        liAbility.addClass("list-group-item");
        liAbility.appendTo(ulAbility);
      }
    }).fail(function(jqxhr, text, error){
    });
  });

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
