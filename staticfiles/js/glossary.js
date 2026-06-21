(function() {
  var filter = document.getElementById("glossary-filter");
  var groups = document.querySelectorAll(".glossary-group");
  var noMatch = document.getElementById("no-term-match");
  var navLinks = document.querySelectorAll(".group-link");
  var filterTimer;

  if (filter) {
    filter.addEventListener("input", function() {
      clearTimeout(filterTimer);
      filterTimer = setTimeout(function() {
        var q = filter.value.toLowerCase().trim();
        var anyVisible = false;

        groups.forEach(function(group) {
          var items = group.querySelectorAll(".term-item");
          var groupVisible = false;
          items.forEach(function(item) {
            var text = item.textContent.toLowerCase();
            var match = !q || text.indexOf(q) !== -1;
            item.style.display = match ? "" : "none";
            if (match) groupVisible = true;
          });
          group.style.display = groupVisible ? "" : "none";
          if (groupVisible) anyVisible = true;
        });

        if (noMatch) {
          noMatch.classList.toggle("hidden", anyVisible);
          document.getElementById("no-term-query").textContent = q ? 'No terms match "' + q + '".' : "";
        }
      }, 150);
    });
  }

  if ("IntersectionObserver" in window && navLinks.length) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var id = entry.target.id;
          navLinks.forEach(function(link) {
            var cls = "bg-red-100 text-red-700 hover:bg-red-200";
            var activeCls = "bg-red-600 text-white hover:bg-red-700";
            link.className = link.className.replace(activeCls, cls);
            if (link.getAttribute("data-target") === id) {
              link.className = link.className.replace(cls, activeCls);
            }
          });
        }
      });
    }, { rootMargin: "-50% 0px -50% 0px" });

    document.querySelectorAll(".glossary-group").forEach(function(g) { observer.observe(g); });
  }

  var backBtn = document.getElementById("back-to-top");
  if (backBtn) {
    var ticking = false;
    window.addEventListener("scroll", function() {
      if (!ticking) {
        requestAnimationFrame(function() {
          if (window.scrollY > 400) {
            backBtn.classList.remove("translate-y-20", "opacity-0", "pointer-events-none");
            backBtn.classList.add("translate-y-0", "opacity-100", "pointer-events-auto");
          } else {
            backBtn.classList.add("translate-y-20", "opacity-0", "pointer-events-none");
            backBtn.classList.remove("translate-y-0", "opacity-100", "pointer-events-auto");
          }
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
    backBtn.addEventListener("click", function() { window.scrollTo({ top: 0, behavior: "smooth" }); });
  }
})();
