const API_URL = "http://localhost:8000/api";
let token = localStorage.getItem("access_token") || null;

// Hàm đăng ký
async function registerUser() {
  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;

  const response = await fetch(`${API_URL}/users/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();
  alert(data.message || "Đăng ký thành công");
}

// Hàm đăng nhập
async function loginUser() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();
  if (response.ok) {
    token = data.access_token;
    localStorage.setItem("access_token", token);
    await fetchUserInfo();
    await fetchSessions();
  } else {
    alert(data.detail || "Đăng nhập thất bại");
  }
}

// Lấy thông tin user
async function fetchUserInfo() {
  const response = await fetch(`${API_URL}/users/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await response.json();

  document.getElementById("user-info").classList.remove("hidden");
  document.getElementById("session-section").classList.remove("hidden");
  document.getElementById("user-email").innerText = `Email: ${data.email}`;
  document.getElementById("user-role").innerText = `Role: ${data.role}`;
}

// Đăng xuất
function logoutUser() {
  localStorage.removeItem("access_token");
  token = null;
  document.getElementById("user-info").classList.add("hidden");
  document.getElementById("session-section").classList.add("hidden");
}

// Tạo session
async function createSession() {
  const name = document.getElementById("session-name").value;
  const response = await fetch(`${API_URL}/sessions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ name }),
  });

  const data = await response.json();
  if (response.ok) {
    alert("Tạo session thành công!");
    await fetchSessions();
  } else {
    alert(data.detail || "Lỗi khi tạo session");
  }
}

// Lấy danh sách sessions
async function fetchSessions() {
  const response = await fetch(`${API_URL}/sessions`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await response.json();

  const sessionList = document.getElementById("session-list");
  sessionList.innerHTML = "";

  data.forEach((session) => {
    const li = document.createElement("li");
    li.innerText = `${session.name} (${session.id})`;
    sessionList.appendChild(li);
  });
}
