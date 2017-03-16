$(function() {
  var activateNavbarItem = function(elementId) {
    var activeItem = $("#navbar-item-list").children("li.active");
    var targetItem = $(elementId);
    activeItem.removeClass("active");
    targetItem.addClass("active");
  };

  var showContent = function(idContent) {
    $(".necco-content").css("display", "none");
    $(idContent).css("display", "");
  };

  $("#navbar-item-passbook").on("click", function() {
    activateNavbarItem("#navbar-item-passbook");
    showContent("#id-necco-content-passbook");
  });
  $("#navbar-item-settings").on("click", function() {
    activateNavbarItem("#navbar-item-settings");
    showContent("#id-necco-content-settings");
  });
  $("#navbar-item-deshilist").on("click", function() {
    activateNavbarItem("#navbar-item-deshilist");
    showContent("#id-necco-content-deshilist");
  });

  $("#navbar-item-passbook").addClass("active");
});
