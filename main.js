/*
 * SPDX-FileCopyrightText: 2026 Tokimi Rover contributors
 * SPDX-License-Identifier: Apache-2.0
 */

(() => {
  "use strict";

  const root = document.documentElement;
  const languageOptions = document.querySelectorAll("[data-language]");
  const yearTarget = document.querySelector("[data-current-year]");
  const signalStage = document.querySelector(".signal-stage");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const defaultLanguage = "zh-TW";

  const normalizeLanguage = (language) => {
    if (typeof language !== "string") {
      return null;
    }

    const normalized = language.trim().toLowerCase();
    if (normalized === "en") {
      return "en";
    }
    if (normalized === "zh-tw" || normalized === "zh-hant") {
      return "zh-TW";
    }
    return null;
  };

  const readUrlLanguage = () => {
    try {
      const url = new URL(window.location.href);
      return normalizeLanguage(url.searchParams.get("lang"));
    } catch {
      return null;
    }
  };

  const readStoredLanguage = () => {
    try {
      return normalizeLanguage(window.localStorage.getItem("tokimi-language"));
    } catch {
      return null;
    }
  };

  const storeLanguage = (language) => {
    try {
      window.localStorage.setItem("tokimi-language", language);
    } catch {
      // The language switch still works when storage is disabled.
    }
  };

  const syncLanguageUrl = (language, historyMode) => {
    try {
      const url = new URL(window.location.href);
      url.searchParams.set("lang", language);
      const nextUrl = `${url.pathname}${url.search}${url.hash}`;
      const currentUrl = `${window.location.pathname}${window.location.search}${window.location.hash}`;

      if (nextUrl === currentUrl) {
        return;
      }

      window.history[historyMode === "push" ? "pushState" : "replaceState"](
        window.history.state,
        "",
        nextUrl,
      );
    } catch {
      // The visible language still changes if history APIs are unavailable.
    }
  };

  let activeLanguage = defaultLanguage;

  const setLanguage = (language) => {
    const useEnglish = language === "en";
    activeLanguage = useEnglish ? "en" : defaultLanguage;
    root.classList.toggle("is-en", useEnglish);
    root.lang = activeLanguage;

    languageOptions.forEach((option) => {
      const isActive = option.dataset.language === activeLanguage;
      option.setAttribute("aria-pressed", String(isActive));
    });
  };

  const activateLanguage = (language, historyMode) => {
    const nextLanguage = normalizeLanguage(language) ?? defaultLanguage;
    setLanguage(nextLanguage);
    storeLanguage(nextLanguage);
    syncLanguageUrl(nextLanguage, historyMode);
  };

  activateLanguage(
    readUrlLanguage() ?? readStoredLanguage() ?? defaultLanguage,
    "replace",
  );

  languageOptions.forEach((option) => {
    option.addEventListener("click", () => {
      const nextLanguage = normalizeLanguage(option.dataset.language);
      if (!nextLanguage || nextLanguage === activeLanguage) {
        return;
      }
      activateLanguage(nextLanguage, "push");
    });
  });

  window.addEventListener("popstate", () => {
    activateLanguage(
      readUrlLanguage() ?? readStoredLanguage() ?? defaultLanguage,
      "replace",
    );
  });

  if (yearTarget) {
    yearTarget.textContent = String(new Date().getFullYear());
  }

  const revealTargets = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window) || reduceMotion.matches) {
    revealTargets.forEach((target) => target.classList.add("is-visible"));
  } else {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) {
            return;
          }
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8%", threshold: 0.08 },
    );

    revealTargets.forEach((target) => revealObserver.observe(target));
  }

  const updateSignalOffset = (event) => {
    if (!signalStage || reduceMotion.matches) {
      return;
    }

    const bounds = signalStage.getBoundingClientRect();
    const relativeX = (event.clientX - bounds.left) / bounds.width - 0.5;
    const relativeY = (event.clientY - bounds.top) / bounds.height - 0.5;
    root.style.setProperty("--shift-x", `${relativeX * 8}px`);
    root.style.setProperty("--shift-y", `${relativeY * 8}px`);
  };

  if (window.matchMedia("(pointer: fine)").matches) {
    signalStage?.addEventListener("pointermove", updateSignalOffset, { passive: true });
    signalStage?.addEventListener("pointerleave", () => {
      root.style.setProperty("--shift-x", "0px");
      root.style.setProperty("--shift-y", "0px");
    });
  }
})();
