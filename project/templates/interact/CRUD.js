function saveNodes() {
    var dataToSend = option_KG.series[0].data;

    fetch('/api/saveNodes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => response.json())
    .then(data => {
        console.log('后端返回的响应数据:', data);
    })
    .catch(error => {
        console.error('发送请求失败:', error);
    });
}

function saveLinks() {
    var dataToSend = option_KG.series[0].links;

    fetch('/api/saveLinks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => response.json())
    .then(data => {
        console.log('后端返回的响应数据:', data);
    })
    .catch(error => {
        console.error('发送请求失败:', error);
    });
}

function sendNodeName(nodeName) {
    // 构造发送给后端的数据
    var dataToSend = {
        "name": nodeName
    };

    // 发送 POST 请求给后端
    fetch('/api/getNodeInfo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => response.json())
    .then(data => {
        console.log('后端返回的响应数据:', data);
    })
    .catch(error => {
        console.error('发送请求失败:', error);
    });
}

var toolbarVisible = false; // 记录工具栏的显示状态

function toggleToolbar() {
    // 获取工具栏容器和按钮
    var toolbar = document.getElementById('toolbar');
    if (toolbarVisible) {
        toolbar.style.display = 'none';
    } else {
        toolbar.style.display = 'block';
    }
    toolbarVisible = !toolbarVisible; // 切换工具栏的显示状态
}

// 当选择框的值改变时触发该函数
function onCategorySelectChange() {
    var nodeCategorySelect = document.getElementById("nodeCategorySelect");
    var fatherContainer = document.getElementById("fatherContainer");
    
    // 如果选择框的值为“学科”，则显示类别输入框，否则隐藏它
    if (nodeCategorySelect.value === "学科") {
        fatherContainer.style.display = "block";
    } else {
        fatherContainer.style.display = "none";
    }
}

var nodeNameSetInitialized = false;
var nodeNameSet = {};

// 创建节点的函数
function createNode() {
    // 获取用户输入的节点信息
    var nodeName = document.getElementById("addNameInput").value.trim();
    var nodeCategory = document.getElementById("nodeCategorySelect").value;
    var father = (nodeCategory === "学科") ? document.getElementById("fatherInput").value.trim() : "计算机科学";

    // 检查输入是否为空
    if (nodeName === "") {
        alert("请输入节点名称");
        return;
    }

    if (!nodeNameSetInitialized) {
        // 初始化辅助对象，将已有节点名称添加到 nodeNameSet 中
        option_KG.series[0].data.forEach(function(node) {
            nodeNameSet[node.name] = false;
        });

        // 将全局变量标记为已初始化
        nodeNameSetInitialized = true;
    }

    if (nodeName in nodeNameSet) {
        alert("已存在同名节点，请输入不同名称");
        return;
    }

    if (father === "") {
        father = "None";
    } else if (!(father in nodeNameSet)) {
        alert("父节点不存在");
        return;
    }

    var nodeSymbolSize = (nodeCategory === "学科") ? 10 : 20;

    // 创建新节点
    var newNode = {
        "name": nodeName,
        "classify": father,
        "fixedName": nodeName,
        "label": {
            "show": true,
            "color": "white",
            "margin": 8
        },
        "symbolSize": nodeSymbolSize,
        "category": nodeCategory
    };
    option_KG.series[0].data.push(newNode);
    
    // 创建新边
    if (father != "None") {
        var newLink = {
            "source": father,
            "target": nodeName,
            "value": (nodeCategory === "学科") ? "\u5b66\u79d1\u7ec4\u6210" : "\u5206\u7c7b",
            "lineStyle": {
                "color": (nodeCategory === "学科") ? "#9966ff" : "#ff3e96"
            }
        };
        option_KG.series[0].links.push(newLink);
    }

    nodeNameSet[nodeName] = false;

    // 构造发送给后端的数据
    var dataToSend = [{
        "category": nodeCategory,
        "name": nodeName,
        "classify": father
    }];

    // 发送 POST 请求给后端
    fetch('/api/addNode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => response.json())
    .then(data => {
        console.log('后端返回的响应数据:', data);
    })
    .catch(error => {
        console.error('发送请求失败:', error);
    });

    // 更新图表数据
    chart_KG.setOption(option_KG);

    // 显示提示框
    alert("成功添加节点：" + nodeName);
    
    saveNodes();
    saveLinks();
};

// 删除节点的函数
function deleteNode() {
    // 获取用户输入的节点名称
    var nodeName = document.getElementById('deleteNameInput').value;

    if (!nodeNameSetInitialized) {
        // 初始化辅助对象，将已有节点名称添加到 nodeNameSet 中
        option_KG.series[0].data.forEach(function(node) {
            nodeNameSet[node.name] = false;
        });

        // 将全局变量标记为已初始化
        nodeNameSetInitialized = true;
    }

    // 检查节点是否存在
    if (!(nodeName in nodeNameSet)) {
        alert("节点不存在");
        return;
    }

    // 遍历删除
    for (var i = 0; i < option_KG.series[0].data.length; i++) {
        if (option_KG.series[0].data[i].name === nodeName) {
            // 从 data 数组中删除节点
            option_KG.series[0].data.splice(i, 1);
            delete nodeNameSet[nodeName];

            // 删除和该节点相关的边
            option_KG.series[0].links = option_KG.series[0].links.filter(function(link) {
                return link.source !== nodeName && link.target !== nodeName;
            });
            break;
        }
    }

    // 更新图表数据
    chart_KG.setOption({
        series: [{
            data: option_KG.series[0].data,
            links: option_KG.series[0].links
        }]
    });

    // 显示提示框
    alert("成功删除节点：" + nodeName);

    saveNodes();
    saveLinks();
}

clickedNodes = []
// 获取表格容器
var tableContainer = document.getElementById('tableContainer');
// 获取表格
var infoTable = document.getElementById('infoTable');
// 获取表格的tbody
var infoTableBody = infoTable.tBodies[0];

// 批量更新
function update() {
    if (!nodeNameSetInitialized) {
        // 初始化辅助对象，将已有节点名称添加到 nodeNameSet 中
        option_KG.series[0].data.forEach(function(node) {
            nodeNameSet[node.name] = false;
        });

        // 将全局变量标记为已初始化
        nodeNameSetInitialized = true;
    }
    // 获取表格容器
    tableContainer = document.getElementById('tableContainer');
    // 获取表格
    infoTable = document.getElementById('infoTable');
    // 获取表格的tbody
    infoTableBody = infoTable.tBodies[0];

    // 显示表格
    tableContainer.style.display = 'block';

    // 改变点击事件
    chart_KG.off('click');
    chart_KG.on('click', function (params) {
        if (params.dataType === 'node' && params.data.category != '领域') {
            var node = params.data;
            if (nodeNameSet[node.name]) { return; }
            nodeNameSet[node.name] = true;
            clickedNodes.push(node);
            var newRow = infoTableBody.insertRow();
            var cell0 = newRow.insertCell();
            var cell1 = newRow.insertCell();
            var cell2 = newRow.insertCell();
            var cell3 = newRow.insertCell();
    
            // cell0 写入 node.name，不能更改
            cell0.textContent = node.name;
            // cell1 初始为空，可输入
            cell1.innerHTML = '<input type="text" class="small-input" id="cell1_' + node.name + '" value=""">';
            // cell2 初始写入 node.classify，可更改
            cell2.innerHTML = '<input type="text" class="small-input" id="cell2_' + node.name + '" value="' + node.classify + '">';
            // 添加删除按钮
            cell3.innerHTML = '<button class="delete-button">-</button>';

            // 给删除按钮绑定点击事件
            var deleteButton = cell3.querySelector(".delete-button");
            deleteButton.style.backgroundColor = '#ff0000'; // 设置背景颜色为红色
            deleteButton.style.color = '#ffffff'; // 设置文字颜色为白色
            deleteButton.style.marginTop = '5px';
            deleteButton.addEventListener('click', function() {
                // 获取所在行
                var row = this.parentNode.parentNode;
                nodeNameSet[row.cells[0].textContent] = false;
                clickedNodes.splice(row.rowIndex - 1, 1);
                // 从表格中删除该行
                row.remove();
            });
        }
    });
}

// 保存更新的节点信息
function saveUpdate() {
    // 构造发送给后端的数据
    var dataToSend = [];

    // 遍历保存在 clickedNodes 中的节点
    clickedNodes.forEach(function(node) {
        // 获取对应的 input 元素
        var nameInput = document.getElementById('cell1_' + node.name);
        var classifyInput = document.getElementById('cell2_' + node.name);
        
        if (nameInput.value != '' && !(nameInput.value in nodeNameSet)) {
            // 更新nodeNameSet
            delete nodeNameSet[node.name];
            nodeNameSet[nameInput.value] = false;

            // 更新dataToSend
            dataToSend.push({"oldName": node.name, "name": nameInput.value});

            // 更新边
            option_KG.series[0].links = option_KG.series[0].links.filter(function(link) {
                if (link.source === node.name) {
                    link.source = nameInput.value;
                } else if (link.target === node.name) {
                    if (classifyInput.value === 'None') {
                        return false; // 删除该条边
                    } else {
                        link.target = nameInput.value;
                        link.source = classifyInput.value;
                    }
                }
                return true;
            });

            // 更新节点名称
            for (var j = 0; j < option_KG.series[0].data.length; j++) {
                var n = option_KG.series[0].data[j];
                if (n.name === node.name) {
                    n.name = nameInput.value;
                    n.classify = classifyInput.value;
                    break;
                }
            }
        } else {
            nodeNameSet[node.name] = false;
            // 更新边
            option_KG.series[0].links = option_KG.series[0].links.filter(function(link) {
                if (link.target === node.name) {
                    if (classifyInput.value === 'None') {
                        return false; // 删除该条边
                    } else {
                        link.source = classifyInput.value;
                    }
                }
                return true;
            });
        }
                
    });

    // 发送 POST 请求给后端
    fetch('/api/updateNode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => response.json())
    .then(data => {
        console.log('后端返回的响应数据:', data);
    })
    .catch(error => {
        console.error('发送请求失败:', error);
    });
    
    // 清空表格的内容
    infoTableBody.innerHTML = '';

    // 隐藏表格和 Save 按钮
    tableContainer.style.display = 'none';

    // 清空 clickedNodes 数组
    clickedNodes = [];

    chart_KG.setOption(option_KG);

    chart_KG.off('click');
    chart_KG.on('click', function (params) {
        if (params.dataType === 'node' && params.data.category === '学科') {
            var node = params.data;
            sendNodeName(node.fixedName);
        }
    });
    
    alert('更新成功！');

    saveNodes();
    saveLinks();
}

// 获取表格容器
tc = document.getElementById('tableContainer1');
// 获取表格
it = document.getElementById('infoTable1');
// 获取表格的tbody
itb = it.tBodies[0]; 

// 增加书签
function addNotes() {
    if (!nodeNameSetInitialized) {
        // 初始化辅助对象，将已有节点名称添加到 nodeNameSet 中
        option_KG.series[0].data.forEach(function(node) {
            nodeNameSet[node.name] = false;
        });

        // 将全局变量标记为已初始化
        nodeNameSetInitialized = true;
    }
    // 获取表格容器
    tc = document.getElementById('tableContainer1');
    // 获取表格
    it = document.getElementById('infoTable1');
    // 获取表格的tbody
    itb = it.tBodies[0]; 

    // 显示表格
    tc.style.display = 'block';

    // 改变点击事件
    chart_KG.off('click');
    chart_KG.on('click', function (params) {
        if (params.dataType === 'node') {
            var node = params.data;
            if (nodeNameSet[node.name]) { return; }
            nodeNameSet[node.name] = true;
            clickedNodes.push(node);
            var newRow = itb.insertRow();
            var cell0 = newRow.insertCell();
            var cell1 = newRow.insertCell();
            var cell2 = newRow.insertCell();
    
            // cell0 写入 node.name，不能更改
            cell0.textContent = node.name;
            // cell1 初始为空，可输入
            cell1.textContent = node.category;
            // 添加删除按钮
            cell2.innerHTML = '<button class="delete-button">-</button>';

            // 给删除按钮绑定点击事件
            var deleteButton = cell2.querySelector(".delete-button");
            deleteButton.style.backgroundColor = '#ff0000'; // 设置背景颜色为红色
            deleteButton.style.color = '#ffffff'; // 设置文字颜色为白色
            deleteButton.style.marginTop = '5px';
            deleteButton.addEventListener('click', function() {
                // 获取所在行
                var row = this.parentNode.parentNode;
                nodeNameSet[row.cells[0].textContent] = false;
                clickedNodes.splice(row.rowIndex - 1, 1);
                // 从表格中删除该行
                row.remove();
            });
        }
    });
}

// 保存书签
function saveNotes() {
    // 遍历保存在 clickedNodes 中的节点
    clickedNodes.forEach(function(node) {
        nodeNameSet[node.name] = false;
        // 标记节点
        for (var j = 0; j < option_KG.series[0].data.length; j++) {
            var n = option_KG.series[0].data[j];
            if (n.name === node.name) {
                n.label.color = "#ffff00";
                break;
            }
        }
    });
    
    // 清空表格的内容
    itb.innerHTML = '';

    // 隐藏表格和 Save 按钮
    tc.style.display = 'none';

    // 清空 clickedNodes 数组
    clickedNodes = [];

    chart_KG.setOption(option_KG);

    chart_KG.off('click');
    chart_KG.on('click', function (params) {
        if (params.dataType === 'node' && params.data.category === '学科') {
            var node = params.data;
            sendNodeName(node.fixedName);
        }
    });
    
    alert('成功添加书签！');

    saveNodes();
}

// 获取表格容器
dtc = document.getElementById('tableContainer2');
// 获取表格
dit = document.getElementById('infoTable2');
// 获取表格的tbody
ditb = dit.tBodies[0]; 

// 增加书签
function addDelete() {
    if (!nodeNameSetInitialized) {
        // 初始化辅助对象，将已有节点名称添加到 nodeNameSet 中
        option_KG.series[0].data.forEach(function(node) {
            nodeNameSet[node.name] = false;
        });

        // 将全局变量标记为已初始化
        nodeNameSetInitialized = true;
    }
    // 获取表格容器
    dtc = document.getElementById('tableContainer2');
    // 获取表格
    dit = document.getElementById('infoTable2');
    // 获取表格的tbody
    ditb = dit.tBodies[0]; 

    // 显示表格
    dtc.style.display = 'block';

    // 改变点击事件
    chart_KG.off('click');
    chart_KG.on('click', function (params) {
        if (params.dataType === 'node' && params.data.label.color == "#ffff00") {
            var node = params.data;
            if (nodeNameSet[node.name]) { return; }
            nodeNameSet[node.name] = true;
            clickedNodes.push(node);
            var newRow = ditb.insertRow();
            var cell0 = newRow.insertCell();
            var cell1 = newRow.insertCell();
            var cell2 = newRow.insertCell();
    
            // cell0 写入 node.name，不能更改
            cell0.textContent = node.name;
            // cell1 初始为空，可输入
            cell1.textContent = node.category;
            // 添加删除按钮
            cell2.innerHTML = '<button class="delete-button">-</button>';

            // 给删除按钮绑定点击事件
            var deleteButton = cell2.querySelector(".delete-button");
            deleteButton.style.backgroundColor = '#ff0000'; // 设置背景颜色为红色
            deleteButton.style.color = '#ffffff'; // 设置文字颜色为白色
            deleteButton.style.marginTop = '5px';
            deleteButton.addEventListener('click', function() {
                // 获取所在行
                var row = this.parentNode.parentNode;
                nodeNameSet[row.cells[0].textContent] = false;
                clickedNodes.splice(row.rowIndex - 1, 1);
                // 从表格中删除该行
                row.remove();
            });
        }
    });
}

// 删除书签
function deleteNotes() {
    // 遍历保存在 clickedNodes 中的节点
    clickedNodes.forEach(function(node) {
        nodeNameSet[node.name] = false;
        // 标记节点
        for (var j = 0; j < option_KG.series[0].data.length; j++) {
            var n = option_KG.series[0].data[j];
            if (n.name === node.name) {
                n.label.color = "white";
                break;
            }
        }
    });
    
    // 清空表格的内容
    ditb.innerHTML = '';

    // 隐藏表格和 Save 按钮
    dtc.style.display = 'none';

    // 清空 clickedNodes 数组
    clickedNodes = [];

    chart_KG.setOption(option_KG);

    chart_KG.off('click');
    chart_KG.on('click', function (params) {
        if (params.dataType === 'node' && params.data.category === '学科') {
            var node = params.data;
            sendNodeName(node.fixedName);
        }
    });
    
    alert('成功删除书签！');

    saveNodes();
}
