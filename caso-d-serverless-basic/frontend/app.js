(() => {
  // Año footer
  const y = document.getElementById("y");
  if (y) y.textContent = String(new Date().getFullYear());

  // Reveal on scroll (con fallback)
  const els = Array.from(document.querySelectorAll(".reveal"));
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) e.target.classList.add("show");
    }, { threshold: 0.12 });
    els.forEach(el => io.observe(el));
  } else {
    els.forEach(el => el.classList.add("show"));
  }

  // ===== Menú móvil =====
  const menuBtn = document.getElementById("menuBtn");
  const navMenu = document.getElementById("navMenu");
  const overlay = document.getElementById("overlay");

  const isMobile = () => window.matchMedia("(max-width: 980px)").matches;

  const openMenu = () => {
    if (!navMenu || !overlay || !menuBtn) return;
    navMenu.classList.add("open");
    overlay.hidden = false;
    menuBtn.setAttribute("aria-expanded", "true");
  };

  const closeMenu = () => {
    if (!navMenu || !overlay || !menuBtn) return;
    navMenu.classList.remove("open");
    overlay.hidden = true;
    menuBtn.setAttribute("aria-expanded", "false");
  };

  if (menuBtn) {
    menuBtn.addEventListener("click", () => {
      const open = navMenu.classList.contains("open");
      if (open) closeMenu(); else openMenu();
    });
  }
  if (overlay) overlay.addEventListener("click", closeMenu);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeMenu();
  });

  if (navMenu) {
    navMenu.addEventListener("click", (e) => {
      const t = e.target;
      if (!isMobile()) return;
      if (t && t.tagName === "A") closeMenu();
    });
  }

  // ===== Toast =====
  const toast = document.getElementById("toast");
  let toastTimer = null;

  const showToast = (msg) => {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 1400);
  };

  // ===== Animación show/hide para bloques Optional =====
  const prefersReduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const animateHide = (el) => {
    if (!el || el.dataset._hidden === "1") return;
    el.dataset._display = el.dataset._display || getComputedStyle(el).display || "block";

    if (prefersReduced) {
      el.style.display = "none";
      el.dataset._hidden = "1";
      return;
    }

    const start = el.getBoundingClientRect().height || el.scrollHeight || 0;
    el.style.overflow = "hidden";
    el.style.height = `${start}px`;
    el.style.opacity = "1";
    el.style.pointerEvents = "none";

    const anim = el.animate(
      [{ height: `${start}px`, opacity: 1 }, { height: "0px", opacity: 0 }],
      { duration: 220, easing: "ease-out", fill: "forwards" }
    );

    anim.onfinish = () => {
      el.style.display = "none";
      el.style.height = "";
      el.style.opacity = "";
      el.style.overflow = "";
      el.style.pointerEvents = "";
      el.dataset._hidden = "1";
    };
  };

  const animateShow = (el) => {
    if (!el) return;

    const computed = getComputedStyle(el).display;
    const isHidden = el.dataset._hidden === "1" || computed === "none" || el.hasAttribute("hidden");
    if (!isHidden) return;

    const display = el.dataset._display || "block";

    if (prefersReduced) {
      el.style.display = display;
      el.removeAttribute("hidden");
      el.dataset._hidden = "0";
      return;
    }

    el.removeAttribute("hidden");
    el.style.display = display;

    const end = el.scrollHeight || 0;

    el.style.overflow = "hidden";
    el.style.height = "0px";
    el.style.opacity = "0";
    el.style.pointerEvents = "none";

    const anim = el.animate(
      [{ height: "0px", opacity: 0 }, { height: `${end}px`, opacity: 1 }],
      { duration: 260, easing: "ease-out", fill: "forwards" }
    );

    anim.onfinish = () => {
      el.style.height = "";
      el.style.opacity = "";
      el.style.overflow = "";
      el.style.pointerEvents = "";
      el.dataset._hidden = "0";
    };
  };

  // ===== Acordeón (funciona con JS) =====
  const accordions = Array.from(document.querySelectorAll(".accordion[data-accordion]"));

  const setAccordionOpen = (acc, open, announce = false) => {
    const btn = acc.querySelector(".acc-summary");
    const panel = acc.querySelector(".acc-panel");
    if (!btn || !panel) return;

    acc.classList.toggle("open", !!open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");

    if (open) animateShow(panel);
    else animateHide(panel);

    if (announce) {
      showToast(open ? "Sección expandida" : "Sección contraída");
    }
  };

  accordions.forEach(acc => {
    const btn = acc.querySelector(".acc-summary");
    const panel = acc.querySelector(".acc-panel");
    if (!btn || !panel) return;

    // Estado inicial: cerrado
    panel.setAttribute("hidden", "");
    btn.setAttribute("aria-expanded", "false");
    acc.classList.remove("open");

    btn.addEventListener("click", () => {
      const isOpen = acc.classList.contains("open");
      setAccordionOpen(acc, !isOpen, true);
    });
  });

  // ===== 3 VISTAS =====
  const viewChip = document.getElementById("viewChip");
  const viewSwitch = document.getElementById("viewSwitch");
  const viewBtns = viewSwitch ? Array.from(viewSwitch.querySelectorAll("[data-view]")) : [];
  const optionalEls = Array.from(document.querySelectorAll(".optional"));

  const LABEL = {
    quick: "👔 Vista: Reclutador",
    normal: "👀 Vista: Normal",
    deep: "🧠 Vista: Profundo"
  };

  const setActiveBtn = (view) => {
    viewBtns.forEach(btn => btn.classList.toggle("active", btn.dataset.view === view));
  };

  const setChip = (view) => {
    if (!viewChip) return;
    viewChip.textContent = LABEL[view] || "Vista: Normal";
  };

  const setView = (view, announce = true) => {
    const v = (view === "quick" || view === "deep") ? view : "normal";

    // Optional: en quick se ocultan, en normal/deep se muestran
    if (v === "quick") optionalEls.forEach(animateHide);
    else optionalEls.forEach(animateShow);

    // Acordeones: en deep los abrimos automático; en normal los dejamos cerrados; en quick da igual (están ocultos)
    accordions.forEach(acc => {
      if (v === "deep") setAccordionOpen(acc, true, false);
      else setAccordionOpen(acc, false, false);
    });

    // UI
    setActiveBtn(v);
    setChip(v);
    localStorage.setItem("portfolioView", v);

    if (announce) {
      showToast(v === "quick" ? "👔 Vista Reclutador activada" :
        v === "deep" ? "🧠 Vista Profundo activada" :
          "👀 Vista Normal activada");
    }
  };

  viewBtns.forEach(btn => {
    btn.addEventListener("click", () => setView(btn.dataset.view));
  });

  const saved = localStorage.getItem("portfolioView") || "normal";
  setView(saved, false);
})();

// ===== Formulario (Demo Serverless: API Gateway + Lambda + DynamoDB) =====
(() => {
  const form = document.getElementById("contactForm");
  if (!form) return;

  const statusEl = document.getElementById("formStatus");

  // 1) Despliega el backend (carpeta /backend) con SAM
  // 2) Copia el output ApiBaseUrl (ej: https://xxxx.execute-api.sa-east-1.amazonaws.com)
  // 3) Pégalo aquí:
  const API_BASE = "https://tc78a6xibg.execute-api.us-east-2.amazonaws.com";

  const setStatus = (msg) => {
    if (!statusEl) return;
    statusEl.textContent = msg;
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Honeypot anti-spam: si este campo viene con algo, ignoramos.
    const fd = new FormData(form);
    const honey = String(fd.get("company") || "").trim();
    if (honey) return;

    if (!API_BASE || API_BASE === "Pega_aqui_tu_ApiBaseUrl") {
      setStatus("⚠️ Falta configurar la URL del API en app.js (API_BASE). Publica el backend y pega el ApiBaseUrl.");
      return;
    }

    const payload = {
      name: String(fd.get("name") || "").trim(),
      email: String(fd.get("email") || "").trim(),
      message: String(fd.get("message") || "").trim(),
    };

    if (!payload.name || !payload.email || !payload.message) {
      setStatus("⚠️ Completa nombre, email y mensaje.");
      return;
    }

    setStatus("Enviando...");

    try {
      const r = await fetch(`${API_BASE.replace(/\/$/, "")}/lead`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await r.json().catch(() => ({}));
      if (!r.ok || !data.ok) {
        throw new Error(data.error || `Error HTTP ${r.status}`);
      }

      setStatus(`Listo ✅ Guardado en DynamoDB (id: ${data.id || "ok"})`);
      form.reset();
    } catch (err) {
      setStatus(`Error ❌ ${err.message}`);
    }
  });
})();
