/* ==========================================================================
   انجمن صنفی حق‌العمل‌کاران گمرکی — رفتارهای تعاملی سایت (Vanilla JS)
   ========================================================================== */
document.addEventListener("DOMContentLoaded", function () {

  /* ---------------- منوی کشویی دسکتاپ/موبایل (کلیک روی آیتم والد) ---------------- */
  function setupDropdownMenu(navRoot) {
    if (!navRoot) return;
    const parents = navRoot.querySelectorAll("li.has-submenu");
    parents.forEach(function (li) {
      const toggle = li.querySelector(":scope > .nav-toggle");
      if (!toggle) return;
      toggle.addEventListener("click", function (e) {
        e.preventDefault();
        const isOpen = li.classList.contains("open");
        parents.forEach(function (other) { other.classList.remove("open"); });
        if (!isOpen) li.classList.add("open");
      });
    });
    // بستن با کلیک بیرون از منو (فقط دسکتاپ)
    document.addEventListener("click", function (e) {
      if (!navRoot.contains(e.target)) {
        parents.forEach(function (li) { li.classList.remove("open"); });
      }
    });
  }
  setupDropdownMenu(document.querySelector("nav.main-nav"));
  setupDropdownMenu(document.querySelector(".mobile-nav"));

  /* ---------------- همبرگر موبایل ---------------- */
  const burger = document.getElementById("burgerBtn");
  const mobileNav = document.getElementById("mobileNav");
  if (burger && mobileNav) {
    burger.addEventListener("click", function () {
      burger.classList.toggle("active");
      mobileNav.classList.toggle("open");
    });
    mobileNav.querySelectorAll("a:not(.nav-toggle)").forEach(function (a) {
      a.addEventListener("click", function () {
        burger.classList.remove("active");
        mobileNav.classList.remove("open");
      });
    });
  }

  /* ==========================================================================
     اسلایدر تمام‌صفحه (Hero Slider) — سه اسلاید با افکت Fade/Slide
     ========================================================================== */
  const slider = document.querySelector(".hero-slider");
  if (slider) {
    const slides = Array.from(slider.querySelectorAll(".slide"));
    const dotsWrap = slider.querySelector(".slider-dots");
    let current = 0;
    let timer = null;

    function goTo(index) {
      slides[current].classList.remove("active");
      if (dotsWrap) dotsWrap.children[current].classList.remove("active");
      current = (index + slides.length) % slides.length;
      slides[current].classList.add("active");
      if (dotsWrap) dotsWrap.children[current].classList.add("active");
    }
    function next() { goTo(current + 1); }
    function prev() { goTo(current - 1); }
    function restartAutoplay() {
      clearInterval(timer);
      timer = setInterval(next, 6000);
    }

    if (dotsWrap) {
      slides.forEach(function (_, i) {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.setAttribute("aria-label", "اسلاید " + (i + 1));
        if (i === 0) dot.classList.add("active");
        dot.addEventListener("click", function () { goTo(i); restartAutoplay(); });
        dotsWrap.appendChild(dot);
      });
    }
    const nextBtn = slider.querySelector(".slider-next");
    const prevBtn = slider.querySelector(".slider-prev");
    if (nextBtn) nextBtn.addEventListener("click", function () { next(); restartAutoplay(); });
    if (prevBtn) prevBtn.addEventListener("click", function () { prev(); restartAutoplay(); });

    slider.addEventListener("mouseenter", function () { clearInterval(timer); });
    slider.addEventListener("mouseleave", restartAutoplay);

    restartAutoplay();
  }

  /* ==========================================================================
     بخش سوالات متداول — اکاردئون با max-height
     ========================================================================== */
  document.querySelectorAll(".faq-item").forEach(function (item) {
    const question = item.querySelector(".faq-question");
    const answer = item.querySelector(".faq-answer");
    if (!question || !answer) return;
    question.addEventListener("click", function () {
      const isOpen = item.classList.contains("open");
      document.querySelectorAll(".faq-item.open").forEach(function (other) {
        if (other !== item) {
          other.classList.remove("open");
          other.querySelector(".faq-answer").style.maxHeight = null;
        }
      });
      if (isOpen) {
        item.classList.remove("open");
        answer.style.maxHeight = null;
      } else {
        item.classList.add("open");
        answer.style.maxHeight = answer.scrollHeight + "px";
      }
    });
  });

  /* ==========================================================================
     نمایش تدریجی المان‌ها هنگام اسکرول (Intersection Observer)
     ========================================================================== */
  const revealTargets = document.querySelectorAll(".reveal, .stat-box, .review-card");
  if ("IntersectionObserver" in window && revealTargets.length) {
    const revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          if (entry.target.classList.contains("stat-box")) animateCounterBox(entry.target);
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    revealTargets.forEach(function (el) { revealObserver.observe(el); });
  } else {
    revealTargets.forEach(function (el) { el.classList.add("in"); });
  }

  /* شمارنده‌ی آمار (دانش‌آموختگان/اساتید/شعب و ...) */
  function animateCounterBox(box) {
    const b = box.querySelector("b[data-count]");
    if (!b) return;
    const target = parseInt(b.getAttribute("data-count"), 10) || 0;
    let cur = 0;
    const step = Math.max(1, Math.floor(target / 60));
    const iv = setInterval(function () {
      cur += step;
      if (cur >= target) { cur = target; clearInterval(iv); }
      b.textContent = toFa(cur) + (b.getAttribute("data-suffix") || "");
    }, 22);
  }
  function toFa(n) {
    const fa = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];
    return String(n).replace(/[0-9]/g, function (d) { return fa[d]; });
  }

  /* ==========================================================================
     نوار خبری فوری — توقف موشن هنگام هاور/فوکوس روی هر خبر
     ========================================================================== */
  const tickerTrack = document.getElementById("tickerTrack");
  if (tickerTrack) {
    tickerTrack.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("mouseenter", function () { tickerTrack.classList.add("paused"); });
      link.addEventListener("mouseleave", function () { tickerTrack.classList.remove("paused"); });
      link.addEventListener("focus", function () { tickerTrack.classList.add("paused"); });
      link.addEventListener("blur", function () { tickerTrack.classList.remove("paused"); });
    });
  }

  /* ==========================================================================
     اسکرول افقی خدمات مکمل (کاروسل)
     ========================================================================== */
  document.querySelectorAll("[data-hscroll]").forEach(function (wrap) {
    const track = wrap.querySelector(".hscroll");
    const nextBtn = wrap.querySelector("[data-hscroll-next]");
    const prevBtn = wrap.querySelector("[data-hscroll-prev]");
    if (!track) return;
    if (nextBtn) nextBtn.addEventListener("click", function () { track.scrollBy({ left: 280, behavior: "smooth" }); });
    if (prevBtn) prevBtn.addEventListener("click", function () { track.scrollBy({ left: -280, behavior: "smooth" }); });
  });

  /* ==========================================================================
     پلیر کتاب صوتی (Play/Pause گرد + جست‌وجو/فیلتر)
     ========================================================================== */
  const audioPlayer = document.querySelector("[data-audio-player]");
  if (audioPlayer) {
    const playBtn = audioPlayer.querySelector("[data-play-btn]");
    const playIcon = audioPlayer.querySelector("[data-play-icon]");
    let isPlaying = false;
    if (playBtn) {
      playBtn.addEventListener("click", function () {
        isPlaying = !isPlaying;
        playBtn.setAttribute("aria-pressed", String(isPlaying));
        playIcon.innerHTML = isPlaying
          ? '<rect x="6" y="5" width="4" height="14"></rect><rect x="14" y="5" width="4" height="14"></rect>'
          : '<path d="M8 5v14l11-7z"></path>';
      });
    }
    const progressBar = audioPlayer.querySelector("[data-progress-bar]");
    const progressFill = audioPlayer.querySelector("[data-progress-fill]");
    if (progressBar && progressFill) {
      progressBar.addEventListener("click", function (e) {
        const rect = progressBar.getBoundingClientRect();
        const pct = Math.round(((e.clientX - rect.left) / rect.width) * 100);
        progressFill.style.width = Math.max(0, Math.min(100, 100 - pct)) + "%";
      });
    }
    const searchInput = audioPlayer.querySelector("[data-book-search]");
    const levelSelect = audioPlayer.querySelector("[data-book-level]");
    const accentSelect = audioPlayer.querySelector("[data-book-accent]");
    const rows = Array.from(audioPlayer.querySelectorAll("[data-book-row]"));
    function filterBooks() {
      const q = (searchInput && searchInput.value || "").trim().toLowerCase();
      const lvl = levelSelect ? levelSelect.value : "";
      const acc = accentSelect ? accentSelect.value : "";
      rows.forEach(function (row) {
        const title = (row.getAttribute("data-title") || "").toLowerCase();
        const level = row.getAttribute("data-level") || "";
        const accent = row.getAttribute("data-accent") || "";
        const match = (!q || title.indexOf(q) !== -1) && (!lvl || level === lvl) && (!acc || accent === acc);
        row.style.display = match ? "" : "none";
      });
    }
    [searchInput, levelSelect, accentSelect].forEach(function (el) {
      if (el) el.addEventListener("input", filterBooks);
    });
  }

  /* ==========================================================================
     بخش شعب — تعویض نقشه با کلیک روی هر شعبه
     ========================================================================== */
  document.querySelectorAll("[data-branch-card]").forEach(function (card) {
    card.addEventListener("click", function () {
      document.querySelectorAll("[data-branch-card]").forEach(function (c) { c.classList.remove("active"); });
      card.classList.add("active");
      const lat = card.getAttribute("data-lat");
      const lng = card.getAttribute("data-lng");
      const mapFrame = document.getElementById("branchMapFrame");
      if (mapFrame && lat && lng) {
        mapFrame.src = "https://maps.google.com/maps?q=" + lat + "," + lng + "&z=15&output=embed";
      }
    });
  });

  /* ==========================================================================
     ثبت نظر دانش‌پذیران — ذخیره در localStorage و نمایش ۴ نظر آخر
     ========================================================================== */
  const REVIEWS_KEY = "khayyam_customs_guild_reviews";
  const reviewForm = document.getElementById("reviewForm");
  const reviewListEl = document.getElementById("reviewList");

  function loadReviews() {
    try {
      const raw = localStorage.getItem(REVIEWS_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (err) {
      return [];
    }
  }
  function saveReviews(list) {
    try { localStorage.setItem(REVIEWS_KEY, JSON.stringify(list)); } catch (err) { /* noop */ }
  }
  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }
  function renderReviews() {
    if (!reviewListEl) return;
    const stored = loadReviews();
    const seed = JSON.parse(reviewListEl.getAttribute("data-seed") || "[]");
    const all = stored.concat(seed).slice(0, 4);
    reviewListEl.innerHTML = all.map(function (r) {
      const initials = (r.name || "؟").trim().charAt(0);
      const stars = "★".repeat(r.rating) + "☆".repeat(5 - r.rating);
      return (
        '<div class="review-card reveal in">' +
          '<div class="review-head">' +
            '<div class="review-avatar">' + escapeHtml(initials) + "</div>" +
            "<div>" +
              '<div class="review-name">' + escapeHtml(r.name) + "</div>" +
              '<div class="review-date">' + escapeHtml(r.date) + "</div>" +
            "</div>" +
            '<div class="review-stars">' + stars + "</div>" +
          "</div>" +
          '<p class="review-text">' + escapeHtml(r.text) + "</p>" +
        "</div>"
      );
    }).join("");
  }
  renderReviews();

  if (reviewForm) {
    reviewForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const name = reviewForm.querySelector("[name=rv_name]").value.trim();
      const email = reviewForm.querySelector("[name=rv_email]").value.trim();
      const ratingInput = reviewForm.querySelector("[name=rv_rating]:checked");
      const text = reviewForm.querySelector("[name=rv_text]").value.trim();
      if (!name || !text || !ratingInput) return;

      const list = loadReviews();
      list.unshift({
        name: name,
        email: email,
        rating: parseInt(ratingInput.value, 10),
        text: text,
        date: new Date().toLocaleDateString("fa-IR"),
      });
      saveReviews(list.slice(0, 20));
      renderReviews();
      reviewForm.reset();
      const successMsg = document.getElementById("reviewSuccessMsg");
      if (successMsg) {
        successMsg.style.display = "block";
        setTimeout(function () { successMsg.style.display = "none"; }, 3000);
      }
    });
  }

  /* ==========================================================================
     داشبورد: باز/بسته کردن سایدبار در موبایل
     ========================================================================== */
  const dashBurger = document.getElementById("dashBurger");
  const dashSidebar = document.getElementById("dashSidebar");
  if (dashBurger && dashSidebar) {
    dashBurger.addEventListener("click", function () {
      dashSidebar.classList.toggle("open");
    });
  }
});
