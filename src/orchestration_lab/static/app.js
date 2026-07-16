const call = async (path, options = {}) => {
  const response = await fetch("/api" + path, Object.assign({
    headers: {"Content-Type": "application/json"}
  }, options));
  if (!response.ok) throw new Error("Falha na execução.");
  return response.json();
};
const safe = value => String(value).replace(/[&<>"']/g, char =>
  ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[char]));
const toast = text => {
  const node = document.querySelector("#toast"); node.textContent = text;
  node.classList.add("show"); setTimeout(() => node.classList.remove("show"), 2600);
};
function renderResult(prefix, result) {
  document.querySelector("#" + prefix + "-time").textContent =
    result.duration_ms + " ms · " + result.mode;
  const steps = result.traces.map(trace =>
    '<div class="step"><span>' + trace.sequence + '</span><div><b>' + safe(trace.role) +
    "</b><p>" + safe(trace.output) + "</p></div></div>"
  ).join("");
  document.querySelector("#" + prefix + "-output").innerHTML =
    steps + '<div class="answer"><b>Entrega final</b><br>' + safe(result.final_answer) + "</div>";
}
async function compare() {
  const objective = document.querySelector("#objective").value.trim();
  if (objective.length < 10) return toast("Descreva uma missão com pelo menos 10 caracteres.");
  const live = document.querySelector("#live").checked;
  const button = document.querySelector("#compare"); button.disabled = true;
  button.textContent = "Orquestrando...";
  try {
    const results = await Promise.all(["crewai", "langgraph"].map(engine =>
      call("/execute", {method:"POST", body:JSON.stringify({engine, objective, live})})
    ));
    renderResult("crew", results[0]); renderResult("lang", results[1]);
    await loadRuns(); toast("Comparação concluída.");
  } catch (error) { toast(error.message); }
  finally { button.disabled = false; button.textContent = "Comparar motores →"; }
}
async function loadRuns() {
  const runs = await call("/runs");
  document.querySelector("#runs").innerHTML = runs.map(run =>
    '<div class="trow"><span>' + safe(run.engine) + "</span><span>" + safe(run.objective) +
    "</span><span>" + safe(run.mode) + "</span><span>" + run.duration_ms +
    " ms</span><span>" + (run.input_tokens + run.output_tokens) + "</span></div>"
  ).join("") || '<div class="empty">Nenhuma execução.</div>';
}
async function capabilities() {
  const data = await call("/capabilities");
  document.querySelector("#mode").textContent = data.live_available
    ? "Groq live available" : "Simulation ready";
  document.querySelector("#live").disabled = !data.live_available;
}
document.querySelector("#compare").onclick = compare;
document.querySelector("#refresh").onclick = loadRuns;
capabilities().catch(() => {}); loadRuns().catch(() => {});

