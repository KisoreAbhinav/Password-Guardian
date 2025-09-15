document.addEventListener('DOMContentLoaded', () => {

    // -------------------- Floating Particles -------------------- //
    function createParticles() {
        const particlesContainer = document.getElementById('particles');
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 15 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 15) + 's';
            particle.style.background = Math.random() > 0.5 ? '#00B2FF' : '#FF5E00';
            particlesContainer.appendChild(particle);
        }
    }
    createParticles();

    // -------------------- Mobile Menu -------------------- //
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');
    menuToggle.addEventListener('click', () => {
        menuToggle.classList.toggle('active');
        navLinks.classList.toggle('active');
    });
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            menuToggle.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });

    // -------------------- Active Navigation -------------------- //
    const sections = document.querySelectorAll('section');
    const navItems = document.querySelectorAll('.nav-link');
    function updateActiveNav() {
        const scrollPosition = window.pageYOffset + 100;
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navItems.forEach(item => item.classList.remove('active'));
                const currentNav = document.querySelector(`.nav-link[href="#${section.id}"]`);
                if (currentNav) currentNav.classList.add('active');
            }
        });
    }
    window.addEventListener('scroll', () => {
        const navbar = document.getElementById('navbar');
        if (window.scrollY > 50) navbar.classList.add('scrolled');
        else navbar.classList.remove('scrolled');
        updateActiveNav();
    });
    updateActiveNav();

    // -------------------- Smooth Scrolling -------------------- //
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    // -------------------- Feature Tabs -------------------- //
    const tabs = document.querySelectorAll('.tab-item');
    const panels = document.querySelectorAll('.content-panel');
    let cyInstance = null;

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.getAttribute('data-tab');
            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(tabId).classList.add('active');

            if (tabId === 'graph' && window.lastGraphData) {
                renderTransitionGraph(window.lastGraphData);
            }
        });
    });

    // -------------------- Contact Form -------------------- //
    document.getElementById('contactForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Message sent! We\'ll get back to you soon.');
        this.reset();
    });

    // -------------------- Glitch Text Rotator -------------------- //
    const textSets = document.querySelectorAll('.text-set');
    let currentIndex = 0;
    textSets.forEach(set => {
        const glitchText = set.querySelector('.glitch-text');
        glitchText.innerHTML = glitchText.textContent.split('').map((char,i)=>
            `<span class="char" style="animation-delay:${i*0.05}s">${char===' ' ? '&nbsp;' : char}</span>`).join('');
    });
    function animateTextIn(set) {
        set.querySelectorAll('.char').forEach(c => c.classList.remove('out'));
        set.querySelector('.subtitle').classList.add('visible');
    }
    function animateTextOut(set) {
        set.querySelectorAll('.char').forEach(c => c.classList.add('out'));
        set.querySelector('.subtitle').classList.remove('visible');
    }
    function rotateText() {
        const currentSet = textSets[currentIndex];
        const nextIndex = (currentIndex+1)%textSets.length;
        const nextSet = textSets[nextIndex];
        animateTextOut(currentSet);
        setTimeout(()=>{
            currentSet.classList.remove('active');
            nextSet.classList.add('active');
            animateTextIn(nextSet);
            currentIndex = nextIndex;
        },600);
    }
    textSets[0].classList.add('active');
    animateTextIn(textSets[0]);
    setInterval(rotateText,5000);

    // -------------------- Password Analyzer -------------------- //
    document.getElementById('analyzeBtn').addEventListener('click', analyzePassword);

    function analyzePassword() {
        const password = document.getElementById('passwordInput').value.slice(0,16);
        if(!password) return alert("Enter a password!");
        const chars = password.split(''), length=chars.length;

        let lowercase=0, uppercase=0, digit=0, special=0;
        chars.forEach(c=>{
            if(c>='a'&&c<='z') lowercase++;
            else if(c>='A'&&c<='Z') uppercase++;
            else if(c>='0'&&c<='9') digit++;
            else special++;
        });

        const categories_present = [lowercase>0, uppercase>0, digit>0, special>0].filter(Boolean).length;

        // Pool size
        let pool_size = 0;
        if(lowercase) pool_size += 26;
        if(uppercase) pool_size += 26;
        if(digit) pool_size += 10;
        if(special) pool_size += 32;

        // Entropy
        const counts={}; chars.forEach(c=>counts[c]=(counts[c]||0)+1);
        let entropy=0; Object.values(counts).forEach(cnt=>{
            let p=cnt/length;
            entropy -= p*Math.log2(p);
        });
        const entropy_score = entropy / Math.log2(pool_size || 2);

        // Edges and edge weights
        const edges=[], edge_weights=[];
        for(let i=0;i<length-1;i++){
            edges.push([chars[i], chars[i+1]]);
            const cat1=getCategory(chars[i]), cat2=getCategory(chars[i+1]);
            let base = chars[i]===chars[i+1]?1.0:(cat1===cat2?0.7:0.4);
            edge_weights.push(base/(length-1));
        }
        const avg_edge_weight = edge_weights.length? edge_weights.reduce((a,b)=>a+b,0)/edge_weights.length : 0;
        const edge_score = 1 - Math.abs(avg_edge_weight - 0.7);

        // Chromatic score
        const nodes = [...new Set(chars)];
        const nodeDegrees = {};
        nodes.forEach(n=>nodeDegrees[n]=0);
        edges.forEach(([a,b])=>{nodeDegrees[a]++; nodeDegrees[b]++;});
        const sortedNodes = nodes.slice().sort((a,b)=>nodeDegrees[b]-nodeDegrees[a]);
        let colorAssignment = {};
        sortedNodes.forEach(n=>{
            let c=0;
            while(Object.values(colorAssignment).includes(c) && edges.some(([x,y])=>(x===n && colorAssignment[y]===c) || (y===n && colorAssignment[x]===c))) c++;
            colorAssignment[n]=c;
        });
        const chromatic_number = Math.max(...Object.values(colorAssignment)) + 1;
        const chromatic_score = nodes.length ? chromatic_number / nodes.length : 0;

        const length_score = Math.min(length/16,1);
        const category_score = categories_present/4;

        // Collision
        const users = 1000;
        const search_space_unique = Math.pow(nodes.length, length);
        const collision_prob = search_space_unique>0 ? 1-Math.exp(-(users*(users-1))/(2*search_space_unique)) : 1;
        const collision_score = 1 - Math.min(collision_prob, 1);

        // -------------------- Permutations & Search Space -------------------- //
        const charCounts = {};
        chars.forEach(c => charCounts[c] = (charCounts[c] || 0) + 1);
        let perm_space = factorial(length);
        Object.values(charCounts).forEach(cnt => { perm_space /= factorial(cnt); });
        const search_space_category = Math.pow(pool_size, length);
        const search_space_unique_chars = Math.pow(nodes.length, length);

        // -------------------- Final Strength Score -------------------- //
        let strengthScore = (
            entropy_score*25 +
            length_score*20 +
            category_score*20 +
            (1-collision_prob)*15 +
            chromatic_score*10 +
            edge_score*10
        );
        strengthScore = Math.min(100, Math.max(0, Math.round(strengthScore)));

        const bar = document.getElementById("strengthBar");
        const text = document.getElementById("strengthText");

        // Smooth animation
        let currentWidth = parseFloat(bar.style.width) || 0;
        let targetWidth = strengthScore;
        let startTime = null;

        function animateBar(timestamp) {
            if (!startTime) startTime = timestamp;
            let progress = (timestamp - startTime) / 800;
            if (progress > 1) progress = 1;

            let newWidth = currentWidth + (targetWidth - currentWidth) * progress;
            bar.style.width = newWidth + "%";

            if (progress < 1) {
                requestAnimationFrame(animateBar);
            } else {
                bar.style.width = targetWidth + "%";
            }
        }
        requestAnimationFrame(animateBar);

        // Color
        if(strengthScore < 40) bar.style.background = "#FF3B3B";
        else if(strengthScore < 70) bar.style.background = "#FFD93B";
        else bar.style.background = "#3BFF5B";

        // Text
        let qualitative = "Weak";
        if(strengthScore >= 40 && strengthScore < 70) qualitative = "Medium";
        else if(strengthScore >= 70) qualitative = "Strong";

        text.textContent = `Password Strength: ${strengthScore}/100 (${qualitative})`;

        // -------------------- Metrics Display (Two Columns) -------------------- //
        const metricsDiv = document.getElementById('metricsOutput');
        metricsDiv.innerHTML='';

        const leftMetrics = [
            {label:"Password", value:password},
            {label:"Length", value:length},
            {label:"Lowercase", value:lowercase},
            {label:"Uppercase", value:uppercase},
            {label:"Digits", value:digit},
            {label:"Special", value:special},
            {label:"Categories Present", value:categories_present},
            {label:"Entropy per character", value:entropy.toFixed(3)},
            {label:"Adjusted Entropy", value:(entropy*length).toFixed(3)}
        ];

        const rightMetrics = [
            {label:"Pool Size", value:pool_size},
            {label:"Category-based Search Space", value:search_space_category},
            {label:"Unique Character Search Space", value:search_space_unique_chars},
            {label:"Distinct Permutations", value:perm_space},
            {label:"Collision Probability", value:(collision_prob*100).toFixed(2)+"%"},
            {label:"Chromatic Number", value:chromatic_number},
            {label:"Average Edge Weight", value:avg_edge_weight.toFixed(3)},
            {label:"Edge Score", value:edge_score.toFixed(3)}
        ];

        const container = document.createElement('div');
        container.style.display = 'flex';
        container.style.justifyContent = 'space-between';
        container.style.flexWrap = 'wrap';

        const leftCol = document.createElement('div');
        leftCol.style.flex = '0 0 48%';
        leftCol.innerHTML = leftMetrics.map(m=>`<p><strong>${m.label}:</strong> ${m.value}</p>`).join('');
        container.appendChild(leftCol);

        const rightCol = document.createElement('div');
        rightCol.style.flex = '0 0 48%';
        rightCol.innerHTML = rightMetrics.map(m=>`<p><strong>${m.label}:</strong> ${m.value}</p>`).join('');
        container.appendChild(rightCol);

        metricsDiv.appendChild(container);

        // -------------------- Radar Chart -------------------- //
        const radarCanvas = document.getElementById('radarChart');
        radarCanvas.width = 400;
        radarCanvas.height = 400;
        const radarCtx = radarCanvas.getContext('2d');
        if(window.radarChart && typeof window.radarChart.destroy==="function") window.radarChart.destroy();

        window.radarChart = new Chart(radarCtx,{
            type:'radar',
            data:{
                labels:["Collision","Entropy","Category","Chromatic","Transition"],
                datasets:[{
                    label:'Metrics',
                    data:[collision_score, entropy_score, category_score, chromatic_score, edge_score],
                    backgroundColor:'rgba(255,94,0,0.3)',
                    borderColor:'#FF5E00',
                    pointBackgroundColor:'#00B2FF'
                }]
            },
            options:{
                responsive:false,
                maintainAspectRatio:false,
                scales:{r:{suggestedMin:0,suggestedMax:1,
                    grid:{color:"rgba(0,178,255,0.2)"},
                    angleLines:{color:"rgba(255,94,0,0.3)"},
                    pointLabels:{color:"#FFFFFF", font:{size:14,family:'Rajdhani'}},
                    ticks:{backdropColor:"transparent", color:"rgba(200,200,200,0.7)", stepSize:0.2, font:{size:12,family:'Rajdhani'}}
                }},
                plugins:{legend:{display:false}}
            }
        });

        window.lastGraphData = {chars, edges};
        renderTransitionGraph(window.lastGraphData);

        renderSuggestions({
            entropy_score,
            length_score,
            category_score,
            edge_score,
            collision_score,
            chromatic_score,
            lowercase,
            uppercase,
            digit,
            special
        });
    }

    function factorial(n) { return n <= 1 ? 1 : n * factorial(n-1); }

    // -------------------- Transition Graph -------------------- //
    function renderTransitionGraph({chars, edges}){
        const cyContainer = document.getElementById('transitionGraph');
        cyContainer.style.width='400px';
        cyContainer.style.height='400px';
        cyContainer.innerHTML='';

        const uniqueChars = [...new Set(chars)];
        const cyNodes = uniqueChars.map(n => {
            let label = n;
            let bgColor = '#FF5E00';
            if(n===' '){ label='␣'; bgColor='#800080'; }
            else if(/[a-z]/.test(n)) bgColor='#2ca02c';
            else if(/[A-Z]/.test(n)) bgColor='#ff7f0e';
            else if(/\d/.test(n)) bgColor='#d62728';
            else bgColor='#1f77b4';
            return {data:{id:'n_'+n.charCodeAt(0),label:label}, style:{'background-color':bgColor}};
        });

        const cyEdges = edges.map(([s,t], idx)=>({data:{id:'e_'+idx,source:'n_'+s.charCodeAt(0),target:'n_'+t.charCodeAt(0)}}));

        if(cyInstance){cyInstance.destroy(); cyInstance=null;}
        cyInstance = cytoscape({
            container: cyContainer,
            elements:[...cyNodes,...cyEdges],
            style:[
                {selector:'node', style:{'background-color':'data(style.background-color)','label':'data(label)','color':'#fff','text-valign':'center','text-halign':'center','font-size':'14px'}},
                {selector:'edge', style:{'width':3,'line-color':'#00B2FF','target-arrow-color':'#00B2FF','target-arrow-shape':'triangle','curve-style':'bezier'}}
            ],
            layout:{name:'grid', rows: Math.ceil(Math.sqrt(uniqueChars.length)), cols: Math.ceil(Math.sqrt(uniqueChars.length)), fit:true, padding:20}
        });

        cyInstance.resize();
        cyInstance.fit();
    }

    // -------------------- Suggestions Renderer -------------------- //
    function renderSuggestions(scores) {
        const {entropy_score,length_score,category_score,edge_score,collision_score,chromatic_score,lowercase,uppercase,digit,special}=scores;
        const suggestionsDiv = document.getElementById('suggestionsOutput');
        suggestionsDiv.innerHTML='';

        let improved=false;
        const suggestions=[];

        if(entropy_score<0.5){suggestions.push("Increase entropy: avoid repeating characters, add more unique symbols."); improved=true;}
        if(length_score<1.0){suggestions.push("Make your password longer (up to 16 characters) to increase security."); improved=true;}
        if(category_score<1.0){
            const missing=[];
            if(lowercase===0) missing.push("lowercase letters");
            if(uppercase===0) missing.push("uppercase letters");
            if(digit===0) missing.push("digits");
            if(special===0) missing.push("special symbols");
            suggestions.push(`Add more character types (${missing.join(", ")}).`);
            improved=true;}
        if(chromatic_score<0.6){suggestions.push("Mix character positions so different types of characters are spread out."); improved=true;}
        if(edge_score<0.7){suggestions.push("Avoid predictable sequences (like aaa, 1234, or abcd)."); improved=true;}
        if(collision_score<0.5){suggestions.push("Use less common characters and longer length to reduce collision risk."); improved=true;}
        if(!improved){suggestions.push("No major improvements needed!");}

        suggestions.forEach(s=>{
            const p=document.createElement("p");
            p.innerHTML=`💡 <span style="color:#fff;">${s}</span>`;
            p.style.marginBottom="10px";
            suggestionsDiv.appendChild(p);
        });
    }

    function getCategory(c){
        if(c>='a'&&c<='z') return 'lower';
        if(c>='A'&&c<='Z') return 'upper';
        if(c>='0'&&c<='9') return 'digit';
        return 'special';
    }

});