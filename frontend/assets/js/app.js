const API = {
  login: "/api/login",
  logout: "/api/logout",
  algorithms: "/api/algorithms",
  uploadImage: "/api/upload/image",
  uploadVideo: "/api/upload/video",
  history: "/api/history",
  logs: "/api/logs",
  docs: "/api/algorithm_docs",
};

const RUN_API_MAP = {
  yolo: "/api/run/yolo",
  segmentation: "/api/run/segmentation",
  mnist: "/api/run/mnist",
  super_resolution: "/api/run/super_resolution",
  action_recognition: "/api/run/action_recognition",
  texture_style: "/api/run/texture_style",
};

async function requestJSON(url, options = {}) {
  const response = await fetch(url, {
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.message || "请求失败");
  }
  return data;
}

function showStatus(elementId, text, type = "info") {
  const element = document.getElementById(elementId);
  if (!element) {
    return;
  }
  element.className = `status ${type}`;
  element.innerText = text;
}

async function logout() {
  await requestJSON(API.logout, { method: "POST" });
  localStorage.removeItem("username");
  window.location.href = "/login.html";
}
