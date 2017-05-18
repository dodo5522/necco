var activateNavbarItem = function(elementId) {
  var activeItem = $("#navbarItemList").children("li.active");
  var targetItem = $(elementId);
  activeItem.removeClass("active");
  targetItem.addClass("active");
};

var hideContent = function() {
  $(".necco-content").css("display", "none");
  $(".overlay").css("display", "");
  $(".loading").css("display", "");
};

var showContent = function(idContent) {
  $(".necco-content").css("display", "none");
  $(".overlay").fadeOut();
  $(".loading").fadeOut();
  $(idContent).fadeIn();
};

var prepareContent = function(type_) {
  activateNavbarItem("#navbarItem" + type_);
  showContent("#content" + type_);

  var content = $("#content" + type_);
  content.empty();

  var table = $("<table>").appendTo(content);
  table.addClass("table");
  table.addClass("table-responsive");
  table.addClass("table-hover");

  return table;
};

var sortRecordsByKana = function(records) {
  return records.sort(
    function(first, second) {
      if(first.lastKanaName > second.lastKanaName) { return 1; }
      else if(first.kana < second.kana) { return -1; }
      else { return 0; }
    })
};
