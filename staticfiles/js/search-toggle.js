(function() {
  var b = document.getElementById("search-btn");
  var s = document.getElementById("search-bar");
  var i = document.getElementById("search-input");
  if (b && s) {
    b.addEventListener("click", function(e) {
      e.stopPropagation();
      s.classList.toggle("hidden");
      if (!s.classList.contains("hidden")) {
        setTimeout(function() { i.focus(); }, 100);
      }
    });
    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape" && !s.classList.contains("hidden")) {
        s.classList.add("hidden");
      }
    });
    document.addEventListener("click", function(e) {
      if (!s.classList.contains("hidden") && !s.contains(e.target) && e.target !== b && !b.contains(e.target)) {
        s.classList.add("hidden");
      }
    });
  }
})();
