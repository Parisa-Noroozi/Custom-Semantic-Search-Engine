const input = document.getElementById("search-input");
const button = document.getElementById("search-button");
const resultsDiv = document.getElementById("results");
const statusDiv = document.getElementById("status");

button.addEventListener("click", search);
input.addEventListener("keydown", function(event){
    if(event.key === "Enter"){
        search();
    }

});

async function search(){

    const query = input.value.trim();

    if(query === ""){
        return;
    }

    resultsDiv.innerHTML = "";
    statusDiv.innerHTML = `
<div class="loading">
    Searching<span class="dots"></span>
</div>
`;

    const start = performance.now();

    try{
          console.log("1");

        const response = await fetch(
            `http://127.0.0.1:8000/search?q=${encodeURIComponent(query)}`
        );
        console.log("2");

        const data = await response.json();
        console.log("3");
        console.log(data);

        const results = data.results;
          console.log("4");

        const intents = data.intents;
        const originalQuery=data.query;
        
        const tokens= data.tokens;

        const expandedTokens = data.expanded_tokens;

        const expansionReason = data.expansion_reason;
        const stats = data.stats;

        renderIntents(intents);


        const end = performance.now();

        statusDiv.innerHTML =
        `Found ${results.length} results in ${(end-start).toFixed(2)} ms`;

        renderDeveloperInfo(originalQuery, tokens, expandedTokens,expansionReason,intents,stats);

        renderResults(results);

    }

    catch(error){
        console.error(error)
        statusDiv.innerHTML="Connection Error";

    }

}

function highlight(text, query) {

    if (!query) return text;

    const words = [...new Set(
        query.toLowerCase().split(/\s+/).filter(Boolean)
    )];

    const regex = new RegExp(`(${words.join("|")})`, "gi");

    return text.replace(regex, "<mark>$1</mark>");
} 


function createResultCard(item, index){

    const card = document.createElement("div");

    card.className = "result-card";

    card.innerHTML = `

        <h3>
        ${index + 1}. ${highlight(item.text, input.value)}
        </h3>

        <hr>

        <p><b>⭐ Final Score:</b> ${item.final_score}</p>

        <p><b>🔎 BM25 Score:</b> ${item.bm25_score}</p>

        <p><b>🧠 Semantic Score:</b> ${item.semantic_score}</p>

        <p><b>🔗 Relation Bonus:</b> +${item.relation_bonus}</p>

        <p><b>🧩 Category Bonus:</b> +${item.category_bonus}</p>

        <p><b>🎯 Query Concepts:</b> ${item.query_concepts.join(", ")}</p>

        <p><b>🎯 Matched Intent:</b> ${item.matched_intents.join(", ")}</p>
<hr>

<p><b>📖 Why was this result selected?</b></p>

<ul>

${item.reason.map(r => `<li>✔ ${r}</li>`).join("")}
</ul>

            <hr>

            <b>⚙ Ranking Formula</b>

            <p>BM25: ${item.bm25_score} × ${item.bm25_weight}</p>

            <p>Semantic: ${item.semantic_score} × ${item.semantic_weight}</p>

            <p>Intent: ${item.intent_bonus} × ${item.intent_weight}</p>

            <p>Expansion: ${item.expansion_bonus} × ${item.expansion_weight}</p>

            <p>Relation Bonus: +${item.relation_bonus}</p>

            <p>Category Bonus: +${item.category_bonus}</p>

            <p><b>Final Score:</b> ${item.final_score}</p>

            <p style="color:#888;">${item.ranking_reason}</p>
            ,`
    return card;

}



function renderResults(results){
    console.log("enter results")
    console.log("RESULT TYPE:", typeof results);

    console.log("IS ARRAY:", Array.isArray(results));

    console.log("RESULT DATA:", results);
    resultsDiv.innerHTML="";

    if(results.length===0){

        resultsDiv.innerHTML = "";
const empty = document.createElement("div");
empty.className = "empty";

empty.innerHTML =
    "<div style='font-size:50px;'>🔍</div>" +
    "<h2>No Results</h2>" +
    "<p>Try another keyword.</p>";

resultsDiv.appendChild(empty);
        return;

    }
    console.log("results");

    const learningResults = [];
    const pdfResults = [];

    const otherResults = [];    

    results.forEach(item=>{

    if(item.matched_intents.includes("Learning")){
        learningResults.push(item);
    }

    else if(item.matched_intents.includes("PDF")){
        pdfResults.push(item);
    }

    else{
        otherResults.push(item);
    }

});

   if(learningResults.length > 0){
    const title=document.createElement("h2");

    title.innerHTML="🧠 Learning Results";

    resultsDiv.appendChild(title);
    learningResults.forEach((item,index)=>{

        resultsDiv.appendChild(
            createResultCard(item,index)
        );
    });

}
    if(pdfResults.length > 0){
    const title=document.createElement("h2");

    title.innerHTML="📄 PDF Results";
    resultsDiv.appendChild(title);

    pdfResults.forEach((item,index)=>{

        resultsDiv.appendChild(
            createResultCard(item,index)
        );

    });

}

    if(otherResults.length > 0){

    const title=document.createElement("h2");

    title.innerHTML="📁 Other Results";
    resultsDiv.appendChild(title);
    otherResults.forEach((item,index)=>{
        resultsDiv.appendChild(
            createResultCard(item,index)
        );

    });

}

}


function getRank(score) {
    if (score > 0.8) return "high";
    if (score > 0.3) return "medium";
    return "low";
}
const suggestionsDiv = document.getElementById("suggestions");

input.addEventListener("input", getSuggestions);

async function getSuggestions() {
    const q = input.value.trim();

    if (!q) {
        suggestionsDiv.innerHTML = "";
        return;
    }

    try {

        const res = await fetch(
            `http://127.0.0.1:8000/suggest?q=${encodeURIComponent(q)}`
        );

        const data = await res.json();

        renderSuggestions(data);

    } catch (err) {
        console.log(err);
    }
}

function renderSuggestions(items) {
    suggestionsDiv.innerHTML = "";

    items.slice(0, 5).forEach(item => {
        const div = document.createElement("div");

        div.className = "suggestion-item";

        div.innerText = item;

        div.onclick = () => {
            input.value = item;
            suggestionsDiv.innerHTML = "";
            search();
        };
        suggestionsDiv.appendChild(div);
    });
}

document.addEventListener("click", function (e) {
    if (e.target !== input) {
        suggestionsDiv.innerHTML = "";
    }
});


function renderIntents(intents) {
    const box = document.getElementById("intent-box");

    box.innerHTML = "";
    if (!intents || intents.length === 0) {
        return;
    }

    box.innerHTML = "<h3>Detected Intent</h3>";
    intents.forEach(item => {

        const div = document.createElement("div");

        div.innerHTML = `👉 ${item[0]} (${item[1]}%)`;

        box.appendChild(div);
    });

}


function renderDeveloperInfo(originalQuery, tokens,expandedTokens,expansionReason,intents,stats){

    const old = document.getElementById("developer-info");
    if(old) old.remove();

    const div=document.createElement("div");

    div.id="developer-info";
    div.className="developer-card";

    div.innerHTML=`

    <h2>🛠 Developer Mode</h2>
    <h3>📊 Search Statistics</h3>
<div class="stats-grid">

    <div class="stat-card">
        <div class="stat-number">${stats.documents_scanned}</div>
        <div class="stat-title">Documents</div>
    </div>

    <div class="stat-card">
        <div class="stat-number">${stats.original_tokens}</div>
        <div class="stat-title">Tokens</div>
    </div>

    <div class="stat-card">
        <div class="stat-number">${stats.expanded_tokens}</div>
        <div class="stat-title">Expanded</div>
    </div>

    <div class="stat-card">
        <div class="stat-number">${stats.added_terms}</div>
        <div class="stat-title">Added Terms</div>
    </div>

    <div class="stat-card">
        <div class="stat-number">${stats.returned_results}</div>
        <div class="stat-title">Results</div>
    </div>

</div>

<hr>

    <hr>

    <h3>Original Query</h3>

    <p>${originalQuery}</p>

    <hr>

    <h3>Tokens</h3>

    <p>${tokens.join(" • ")}</p>


    <h3>Expanded Query</h3>
    <p>${expandedTokens.join("  •  ")}</p>

    <h3>Expansion Details</h3>
        ${
        Object.entries(expansionReason).map(([key, values]) => `

        <div class="expansion-box">

        <b>${key}</b>

       <div style="font-size:22px;text-align:center;">
        ⬇
        </div>

        <p>
        ${values.join("<br>")}
        </p>

        <br>

        <span style="color:#888;">
        Dictionary Expansion
        </span>

        </div>

        `).join("")
        }


    <hr>
    <h3>Detected Intents</h3>
   
    ${intents.map(i=>`
        <p>🧠 ${i[0]} (${i[1]}%)</p>
    `).join("")}

    <hr>
    <h3>Search Pipeline</h3>
    <p>✔ Tokenization</p>
    <p>✔ Intent Detection</p>
    <p>✔ BM25 Ranking</p>
    <p>✔ Intent Re-ranking</p>

    `;
    resultsDiv.parentNode.insertBefore(div,resultsDiv);

}