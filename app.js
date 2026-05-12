const metricLabels = [
  ["pending_count", "待處理"],
  ["blocked_count", "阻塞"],
  ["completed_count", "已完成"],
  ["decision_needed_count", "需決策"],
  ["active_agent_count", "活躍代理"],
];

function formatDateLabel(value) {
  if (!value) return "未提供";
  const date = new Date(`${value}T00:00:00+08:00`);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("zh-TW", {
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "short",
    timeZone: "Asia/Taipei",
  }).format(date);
}

function relativeStatus(metrics) {
  if (!metrics) return "無資料";
  if ((metrics.blocked_count || 0) > 0) return "有阻塞";
  if ((metrics.pending_count || 0) > 0) return "待跟進";
  if ((metrics.completed_count || 0) > 0) return "進展中";
  return "空狀態";
}

function fillMetrics(metrics) {
  const container = document.getElementById("metric-grid");
  const template = document.getElementById("metric-template");

  metricLabels.forEach(([key, label]) => {
    const node = template.content.firstElementChild.cloneNode(true);
    node.querySelector(".metric-label").textContent = label;
    node.querySelector(".metric-value").textContent = metrics?.[key] ?? 0;
    container.appendChild(node);
  });
}

function fillPriorities(priorities) {
  const container = document.getElementById("priority-list");
  const template = document.getElementById("priority-template");

  priorities.forEach((item, index) => {
    const node = template.content.firstElementChild.cloneNode(true);
    node.querySelector(".priority-index").textContent = String(index + 1).padStart(2, "0");
    node.querySelector("h3").textContent = item.title;
    node.querySelector(".source-chip").textContent = item.source_agent;
    node.querySelector(".priority-reason").textContent = item.reason;
    node.querySelector(".priority-next").textContent = `下一步：${item.next_step}`;
    container.appendChild(node);
  });
}

function fillCalendar(items) {
  const container = document.getElementById("calendar-list");
  const template = document.getElementById("calendar-template");

  items.forEach((item) => {
    const node = template.content.firstElementChild.cloneNode(true);
    node.querySelector(".calendar-time").textContent = item.time_range;
    node.querySelector("h3").textContent = item.related_event;
    node.querySelector(".calendar-impact").textContent = item.affected_item;
    node.querySelector(".calendar-priority").textContent = item.suggested_priority;
    container.appendChild(node);
  });
}

function fillUpdates(items) {
  const container = document.getElementById("agent-updates");
  const template = document.getElementById("update-template");

  items.forEach((item) => {
    const node = template.content.firstElementChild.cloneNode(true);
    node.querySelector("h3").textContent = item.agent_name;
    node.querySelector(".update-summary").textContent = item.summary;
    node.querySelector(".update-status").textContent = `${item.latest_status} · ${item.confidence}`;
    node.querySelector(".update-next").textContent = `下一步：${item.next_step}`;
    node.querySelector(".update-source").textContent = `${item.report_date} · ${item.source_file}`;
    container.appendChild(node);
  });
}

function fillRisks(items) {
  const container = document.getElementById("risk-list");
  const template = document.getElementById("risk-template");

  items.forEach((item) => {
    const node = template.content.firstElementChild.cloneNode(true);
    node.querySelector("h3").textContent = item.risk_description;
    node.querySelector(".risk-impact").textContent = `影響範圍：${item.impact_scope}`;
    node.querySelector(".risk-action").textContent = item.needs_human_intervention
      ? "需要人工介入"
      : "目前不需要人工介入";
    container.appendChild(node);
  });
}

function fillFollowups(items) {
  const container = document.getElementById("followup-list");
  const template = document.getElementById("followup-template");

  items.forEach((item) => {
    const node = template.content.firstElementChild.cloneNode(true);
    node.querySelector("h3").textContent = item.item;
    node.querySelector(".followup-owner").textContent = `來源：${item.owner_source}`;
    node.querySelector(".followup-time").textContent = `建議跟進時間：${item.suggested_follow_up_time}`;
    container.appendChild(node);
  });
}

function renderDashboard(data) {
  document.getElementById("rail-date").textContent = formatDateLabel(data.date);
  document.getElementById("rail-status").textContent = relativeStatus(data.key_metrics);
  document.getElementById("last-updated").textContent = data.date;
  document.getElementById("top-summary").textContent = data.top_summary;

  fillMetrics(data.key_metrics || {});
  fillPriorities(data.today_priorities || []);
  fillCalendar(data.calendar_alignment || []);
  fillUpdates(data.agent_updates || []);
  fillRisks(data.risks_and_alerts || []);
  fillFollowups(data.follow_ups || []);
}

async function loadDashboard() {
  try {
    const response = await fetch("./dashboard/data/latest.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Failed to load dashboard: ${response.status}`);
    }
    const data = await response.json();
    renderDashboard(data);
  } catch (error) {
    document.getElementById("top-summary").textContent = "目前無法讀取 dashboard 資料。";
    document.getElementById("rail-status").textContent = "讀取失敗";
    document.getElementById("last-updated").textContent = "error";
    console.error(error);
  }
}

loadDashboard();
