/**
 * CSDC subtle motion: count-up stats and on-scroll reveals.
 * All effects are opt-in via markup hooks, gated on `html.js`, and fully
 * disabled under prefers-reduced-motion so the site stays calm and accessible.
 */
(function () {
  "use strict";

  var reduceMotion =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hasIO = "IntersectionObserver" in window;

  /* ---- Count-up for the homepage stats (e.g. "160+") ---- */
  function runCount(el) {
    var target = parseInt(el.getAttribute("data-count-to"), 10) || 0;
    var suffix = el.getAttribute("data-count-suffix") || "";
    if (reduceMotion || target === 0) {
      el.textContent = target + suffix;
      return;
    }
    var duration = 1000;
    var startTime = null;
    function tick(now) {
      if (startTime === null) startTime = now;
      var progress = Math.min((now - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
      el.textContent = Math.round(target * eased) + suffix;
      if (progress < 1) window.requestAnimationFrame(tick);
    }
    window.requestAnimationFrame(tick);
  }

  var counters = Array.prototype.slice.call(
    document.querySelectorAll("[data-count-to]")
  );
  // Reset to zero up front so the final value doesn't flash before animating.
  if (!reduceMotion) {
    counters.forEach(function (el) {
      el.textContent = "0" + (el.getAttribute("data-count-suffix") || "");
    });
  }
  if (hasIO && counters.length) {
    var countObserver = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            runCount(entry.target);
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach(function (el) {
      countObserver.observe(el);
    });
  } else {
    counters.forEach(runCount);
  }

  /* ---- On-scroll reveal for sections marked .csdc-reveal ---- */
  var reveals = Array.prototype.slice.call(
    document.querySelectorAll(".csdc-reveal")
  );
  if (reduceMotion || !hasIO) {
    reveals.forEach(function (el) {
      el.classList.add("is-visible");
    });
  } else if (reveals.length) {
    var revealObserver = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    reveals.forEach(function (el) {
      revealObserver.observe(el);
    });
  }

  /* ---- Past-events teaser carousel: auto-rotate the slides ---- */
  var carousels = Array.prototype.slice.call(
    document.querySelectorAll("[data-pe-carousel]")
  );
  carousels.forEach(function (track) {
    var slides = Array.prototype.slice.call(
      track.querySelectorAll(".csdc-pe-carousel-slide")
    );
    if (slides.length < 2 || reduceMotion) {
      return;
    }
    var index = 0;
    window.setInterval(function () {
      slides[index].classList.remove("is-active");
      index = (index + 1) % slides.length;
      slides[index].classList.add("is-active");
    }, 4500);
  });
})();
