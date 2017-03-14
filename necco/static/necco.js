$(function() {
  var activateNavbarItem = function(elementId) {
    var activeItem = $("#navbar-item-list").children("li.active");
    var targetItem = $(elementId);
    activeItem.removeClass("active");
    targetItem.addClass("active");
  };

  $("#navbar-item-main").on("click", function() {
    activateNavbarItem("#navbar-item-main");
  });
  $("#navbar-item-settings").on("click", function() {
    activateNavbarItem("#navbar-item-settings");
  });
  $("#navbar-item-userlist").on("click", function() {
    activateNavbarItem("#navbar-item-userlist");
  });

  $("#navbar-item-main").addClass("active");
});
