// Global state
let currentUser = {
  email: "freeediting35@gmail.com",
  credits: 10000,
  plan: "agency"
};

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
  fetchUserData();
  setupEventListeners();
  loadDigitalProducts();
  loadAnalytics();
});

async function fetchUserData() {
  try {
    const res = await fetch(`/api/auth/me?email=${encodeURIComponent(currentUser.email)}`);
    const data = await res.json();
    if (data.status === "success") {
      currentUser = data.user;
      updateUserUI();
    }
  } catch (err) {
    console.warn("Could not fetch user profile, using local defaults:", err);
  }
}

function updateUserUI() {
  const creditBadge = document.getElementById("user-credits");
  if (creditBadge) {
    creditBadge.textContent = `${currentUser.credits} Credits`;
  }
  const planBadge = document.getElementById("user-plan");
  if (planBadge) {
    planBadge.textContent = currentUser.plan.toUpperCase();
  }
}

function setupEventListeners() {
  // Video Generator Form
  const genForm = document.getElementById("video-gen-form");
  if (genForm) {
    genForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      await handleGenerateVideo();
    });
  }

  // Hook Analyzer Form
  const hookForm = document.getElementById("hook-analyzer-form");
  if (hookForm) {
    hookForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      await handleAnalyzeHook();
    });
  }

  // Security Recon Form
  const reconForm = document.getElementById("recon-scan-form");
  if (reconForm) {
    reconForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      await handleReconScan();
    });
  }
}

async function handleGenerateVideo() {
  const topic = document.getElementById("gen-topic").value;
  const niche = document.getElementById("gen-niche").value;
  const duration = parseInt(document.getElementById("gen-duration").value, 10);
  const subtitleStyle = document.getElementById("gen-sub-style").value;
  const btn = document.getElementById("btn-generate");

  if (!topic) return alert("Please enter a video topic!");

  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> Synthesizing Viral Script & Prompts...`;

  try {
    const res = await fetch("/api/generate/full-bundle", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_email: currentUser.email,
        topic: topic,
        niche: niche,
        target_duration: duration,
        subtitle_style: subtitleStyle
      })
    });

    const data = await res.json();
    if (data.status === "success") {
      currentUser.credits = data.remaining_credits;
      updateUserUI();
      renderGeneratedOutput(data);
    } else {
      alert(data.detail || "Generation error");
    }
  } catch (err) {
    alert("API error: " + err.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `⚡ Generate Viral Storyboard & Prompts (25 Credits)`;
  }
}

function renderGeneratedOutput(data) {
  const outputContainer = document.getElementById("generation-results");
  if (!outputContainer) return;

  outputContainer.style.display = "block";

  // Render Hooks
  const hooksContainer = document.getElementById("hook-variations");
  if (hooksContainer) {
    hooksContainer.innerHTML = data.script_data.hook_variations.map(h => `
      <div class="glass-card" style="padding: 16px; margin-bottom: 12px; border-left: 4px solid var(--accent-purple);">
        <div style="display:flex; justify-content:space-between; margin-bottom: 6px;">
          <span style="font-size:0.8rem; font-weight:700; color:var(--accent-purple);">${h.type}</span>
          <span style="font-size:0.8rem; background:rgba(16,185,129,0.15); color:var(--accent-green); padding:2px 8px; border-radius:12px; font-weight:700;">Score: ${h.retention_score}</span>
        </div>
        <p style="font-size:0.95rem; font-weight:600; color:#fff;">"${h.hook_text}"</p>
      </div>
    `).join("");
  }

  // Render Storyboard Scenes
  const scenesContainer = document.getElementById("storyboard-scenes");
  if (scenesContainer) {
    scenesContainer.innerHTML = data.script_data.scenes.map(s => `
      <div class="glass-card" style="padding: 18px; margin-bottom: 16px;">
        <div style="display:flex; justify-content:space-between; margin-bottom: 8px;">
          <span style="font-weight:700; font-size:0.9rem; color:#c4b5fd;">Scene ${s.scene_number}: ${s.scene_type}</span>
          <span style="font-size:0.8rem; color:var(--text-dim);">${s.timestamp}</span>
        </div>
        <div style="margin-bottom: 8px; font-size:0.9rem;">
          <strong style="color:var(--text-muted);">Voiceover:</strong> "${s.voiceover}"
        </div>
        <div style="background:rgba(0,0,0,0.4); padding:10px; border-radius:6px; font-family:monospace; font-size:0.82rem; color:#38bdf8; word-break:break-all;">
          <strong>🎬 Veo 3 / Kling Prompt:</strong> ${s.video_ai_prompt}
        </div>
      </div>
    `).join("");
  }

  // Update Live Phone Mockup
  const captionEl = document.getElementById("mockup-caption");
  if (captionEl && data.script_data.hook_variations[0]) {
    captionEl.innerHTML = `<span class="highlight">STOP!</span> ${data.script_data.hook_variations[0].hook_text}`;
  }

  outputContainer.scrollIntoView({ behavior: "smooth" });
}

async function handleAnalyzeHook() {
  const scriptText = document.getElementById("hook-text-input").value;
  if (!scriptText) return;

  const res = await fetch("/api/generate/analyze-hooks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ script_text: scriptText })
  });

  const data = await res.json();
  if (data.status === "success") {
    const a = data.analysis;
    document.getElementById("analysis-output").innerHTML = `
      <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 16px;">
        <div class="glass-card" style="text-align:center; padding: 12px;">
          <div style="font-size:0.8rem; color:var(--text-dim);">Grade</div>
          <div style="font-size:1.6rem; font-weight:800; color:var(--accent-green);">${a.hook_strength_grade}</div>
        </div>
        <div class="glass-card" style="text-align:center; padding: 12px;">
          <div style="font-size:0.8rem; color:var(--text-dim);">Retention Prob</div>
          <div style="font-size:1.6rem; font-weight:800; color:var(--accent-purple);">${a.retention_probability}</div>
        </div>
        <div class="glass-card" style="text-align:center; padding: 12px;">
          <div style="font-size:0.8rem; color:var(--text-dim);">Scroll-Stop</div>
          <div style="font-size:1.6rem; font-weight:800; color:var(--accent-cyan);">${a.scroll_stop_index}/10</div>
        </div>
      </div>
    `;
  }
}

async function handleReconScan() {
  const domain = document.getElementById("recon-target").value;
  const btn = document.getElementById("btn-recon-scan");
  if (!domain) return alert("Enter a target domain");

  btn.disabled = true;
  btn.textContent = "Scanning Attack Surface...";

  try {
    const res = await fetch("/api/recon/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_domain: domain, scan_depth: "deep" })
    });
    const data = await res.json();
    if (data.status === "success") {
      document.getElementById("recon-results").style.display = "block";
      document.getElementById("recon-subdomains").innerHTML = data.subdomains_found.map(s => `<li>${s}</li>`).join("");
      document.getElementById("recon-findings").innerHTML = data.findings.map(f => `
        <div class="glass-card" style="margin-bottom: 12px; padding: 16px;">
          <div style="display:flex; justify-content:space-between;">
            <strong style="color:${f.severity === 'High' ? '#ef4444' : '#f59e0b'};">[${f.severity}] ${f.vuln_type}</strong>
            <span style="color:var(--accent-green); font-weight:700;">Potential: ${f.bounty_potential}</span>
          </div>
          <p style="font-size:0.88rem; color:var(--text-muted); margin-top:6px;">${f.description}</p>
        </div>
      `).join("");
    }
  } catch (err) {
    alert("Recon failed: " + err.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "🔍 Run Attack Surface Recon";
  }
}

async function loadDigitalProducts() {
  const container = document.getElementById("digital-products-grid");
  if (!container) return;

  try {
    const res = await fetch("/api/products/list");
    const data = await res.json();
    if (data.status === "success") {
      container.innerHTML = data.products.map(p => `
        <div class="glass-card pricing-card">
          <div>
            <span style="font-size:0.75rem; text-transform:uppercase; color:var(--accent-cyan); font-weight:700;">${p.category}</span>
            <h3 style="margin: 8px 0; font-size:1.25rem;">${p.title}</h3>
            <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom: 16px;">${p.description}</p>
            <div class="price">$${p.price_usd} <span>USD</span></div>
            <ul class="feature-list">
              ${(p.features || []).map(f => `<li>${f}</li>`).join("")}
            </ul>
          </div>
          <button class="btn btn-primary" style="width:100%; margin-top:20px;" onclick="buyProduct('${p.slug}', '${p.title}', ${p.price_usd})">
            ⚡ Instant Download ($${p.price_usd})
          </button>
        </div>
      `).join("");
    }
  } catch (err) {
    console.error("Error loading products:", err);
  }
}

async function buyProduct(slug, title, price) {
  if (confirm(`Purchase and download "${title}" for $${price}?`)) {
    try {
      const res = await fetch("/api/products/purchase", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product_slug: slug, customer_email: currentUser.email })
      });
      const data = await res.json();
      if (data.status === "success") {
        alert(`Payment Verified! Download starting: ${data.message}`);
        window.open(data.download_url, "_blank");
      }
    } catch (err) {
      alert("Purchase failed: " + err.message);
    }
  }
}

async function subscribePlan(planKey) {
  if (confirm(`Upgrade to ${planKey.toUpperCase()} plan?`)) {
    try {
      const res = await fetch("/api/billing/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_email: currentUser.email, plan: planKey })
      });
      const data = await res.json();
      if (data.status === "success") {
        alert(data.message);
        currentUser = data.user;
        updateUserUI();
      }
    } catch (err) {
      alert("Subscription failed: " + err.message);
    }
  }
}

async function loadAnalytics() {
  const mrrEl = document.getElementById("stat-mrr");
  const revEl = document.getElementById("stat-rev");
  const usersEl = document.getElementById("stat-users");

  try {
    const res = await fetch("/api/analytics/overview");
    const data = await res.json();
    if (data.status === "success") {
      const m = data.metrics;
      if (mrrEl) mrrEl.textContent = `$${m.mrr_usd.toLocaleString()}`;
      if (revEl) revEl.textContent = `$${m.total_revenue_usd.toLocaleString()}`;
      if (usersEl) usersEl.textContent = m.active_creators;
    }
  } catch (err) {
    console.warn("Analytics fetch skipped:", err);
  }
}
