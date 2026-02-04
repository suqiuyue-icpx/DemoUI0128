var logs = [];

let clickTimer = null;
let lastClickTime = 0
let currentParentNode = null;
let ancestorTdNode = null;

let _target;
document.addEventListener('mousedown', function(event) {
  _target = event.target;
}, true);

// 监听单击事件（需要延迟处理）
document.addEventListener('click', function(event) {
    currentParentNode = event.target.parentElement;
    ancestorTdNode = event.target.closest('td');
    // 获取相对于屏幕的坐标
//    const screenX = event.screenX;
//    const screenY = event.screenY;
//    console.log('相对于屏幕的坐标:', screenX, screenY);
    // 如果双击事件已触发，则跳过单击处理
    const now = Date.now();
    if (now - lastClickTime < 300) {
        // 认为是双击的一部分，跳过
        lastClickTime = 0;
        return;
    }
    lastClickTime = now;
    let target = event.target;
    if (target !== _target) {
        target = _target;
        _target = null;
    }
    console.log('进入监听单击事件click方法');
    clickTimer = setTimeout(() => {
        test({
            target,
        }, 'click');
    }, 200);
}, true);

// 监听双击事件
document.addEventListener('dblclick', function(event) {
  // 取消未执行的单击事件定时器
  clearTimeout(clickTimer);
  // 标记双击事件已触发
  handleElementAction(event, 'double_click');
}, true);

// 监听右键事件（上下文菜单事件）
document.addEventListener('contextmenu', function(event) {
    handleElementAction(event, 'click_right');
}, true);

// 监听输入事件
document.addEventListener('input', function(event) {
    console.log('输入事件');
    var element = event.target;
    var xpath = '';
    var operationText = '';
    var action = 'input';
    var value = event.target.value;
    var attributes = {};

    if (element) {
        var ancestorTabid = getAncestorWithTabidXPath(element);
        var ancestoroperationText = getInputLabel(element);
        if (ancestorTabid) {
            xpath = ancestorTabid;
            operationText = ancestoroperationText;
        }
    }

    if (xpath) {
        console.log(xpath);
        logs.push({
            validate: isLocatorUnique(xpath),
            action: action,
            xpath: xpath,
            operationText: operationText,
            attributes: attributes,
            value: value
        });
        for (let i = 0; i < element.attributes.length; i++) {
            var attr = element.attributes[i];
            if (attr.value) {
                logs[logs.length - 1].attributes[attr.name] = attr.value;
            }
        }
    }
}, true);


function isLocatorUnique(xpath) {
  try {
    const result = document.evaluate(
      xpath,
      document,
      null,
      XPathResult.ORDERED_NODE_ITERATOR_TYPE,
      null
    );
    let count = 0;
    let node;
    while ((node = result.iterateNext()) !== null) {
      count++;
    }
    return count === 1;
  } catch (error) {
    console.error('XPath执行错误:', error);
    return false;
  }
}

// 通用处理函数
function test(event, actionType) {
    if (!event || !event.target) {
        console.error("Invalid event object:", event);
        return;
    }

    var element = event.target;
    var action = actionType === 'click' ? 'click' : actionType === 'double_click' ? 'double_click' : 'click_right';
    var operationText = '';
    var xpath = '';
    var attributes = {};

    //section[@class="ant-layout"]//main//div[contains(@class,"list-query-form")]//form--- JS 写法section[class="ant-layout//main//div[class*="list-query-form"]//form
    const ancestorDocument = element.parentElement?.closest('div[role="document"]');
    const ancestorSection = element.closest('section[class*="ant-layout"]');
    const ancestorPage = ancestorSection ? ancestorSection.querySelector('main') : null;

    // 提前返回条件判断
    if (!ancestorDocument && !ancestorPage) return null;
    let pElement = ancestorPage ?? ancestorDocument ?? null;

    if (ancestorPage) {
        xpath_list = getAllElementXpath(pElement);
        console.log('进入监听单击事件test→ancestorPage方法', xpath_list, ancestorPage);

        // 检查xpath_list是否为数组（当element.tagName === 'MAIN'时返回数组）
        if (Array.isArray(xpath_list)) {
            // 遍历数组中的每个input元素信息
            xpath_list.forEach(function(inputInfo) {
                // 从inputInfo中获取信息
                action = 'input';
                var id = inputInfo.id;
                xpath = `//section[@class="ant-layout"]//main//div[contains(@class,"list-query-form")]//form//input[@id='${id}']`;
                operationText = inputInfo.placeholder;
                attributes = inputInfo.type
                
                if (xpath) {
                    console.log(xpath);
                    logs.push({
                        validate: isLocatorUnique(xpath),
                        action: action,
                        xpath: xpath,
                        operationText: operationText,
                        attributes: attributes
                    });
                }
            });
        } else {
            // 处理非数组情况（当element.tagName !== 'MAIN'时返回对象）
            xpath = xpath_list['xpath'];
            operationText = xpath_list['operationText'];
            if (xpath) {
                console.log(xpath);
                logs.push({
                    validate: isLocatorUnique(xpath),
                    action: action,
                    xpath: xpath,
                    operationText: operationText,
                    attributes: attributes
                });
            }
        }
    }else if(ancestorDocument) {
        xpath_list = getAllElementXpath(pElement);
        console.log('进入监听单击事件test→ancestorDocument方法', xpath_list, ancestorDocument);

        // 检查xpath_list是否为数组（当element.tagName === 'MAIN'时返回数组）
        if (Array.isArray(xpath_list)) {
            // 遍历数组中的每个input元素信息
            xpath_list.forEach(function(inputInfo) {
                // 从inputInfo中获取信息
                action = 'input';
                var id = inputInfo.id;
                xpath = inputInfo.xpath;
                operationText = inputInfo.placeholder;
                attributes = inputInfo.type

                if (xpath) {
                    console.log(xpath);
                    logs.push({
                        validate: isLocatorUnique(xpath),
                        action: action,
                        xpath: xpath,
                        operationText: operationText,
                        attributes: attributes
                    });
                }
            });
        } else {
            // 处理非数组情况（当element.tagName !== 'MAIN'时返回对象）
            xpath = xpath_list['xpath'];
            operationText = xpath_list['operationText'];
            if (xpath) {
                console.log(xpath);
                logs.push({
                    validate: isLocatorUnique(xpath),
                    action: action,
                    xpath: xpath,
                    operationText: operationText,
                    attributes: attributes
                });
            }
        }
    }
}

function getAllElementXpath(element) {
    console.log('当前页面对象', element.tagName)
    var xpath = '';
    var operationText = '';
    if(element.tagName === 'DIV') {
        // 假设 ancestorQueryList  ancestorQueryTable 已通过 closest 方法获取
        var ancestorForm = element.querySelector('form');
        var modeName = ancestorForm ? ancestorForm.getAttribute('__unique_key__') : null ;

        // 步骤1：检查 ancestorForm 是否存在
        if (ancestorForm) {
            var ancestorDiv = ancestorForm.querySelector(`div[locale*="${modeName}"]`);
            var inputInfoArray = [];
            // 步骤2：获取所有表单项元素
            var formItems = ancestorForm.querySelectorAll('div[class*="ant-row ant-form-item"]');

            // 步骤3：遍历表单项元素
            formItems.forEach(function(item, index) {
                // 获取名称div和参数div
                var labelDiv = item.querySelector('div[class="ant-col ant-form-item-label"]');
                var controlDiv = item.querySelector('div[class="ant-col ant-form-item-control"]');

                // 检查必要元素是否存在
                if (labelDiv && controlDiv) {
                    // 获取input元素
                    var inputElement = controlDiv.querySelector('input');

                    if (inputElement) {
                        // 获取名称（从labelDiv中）
                        var name = labelDiv.textContent.trim() || labelDiv.querySelector('div').getAttribute('title') || '';
                        // 获取参数（从input元素中）
                        var type = inputElement.type || 'text';
                        var id = inputElement.id || '';
                        var xpath = `//div[@role="document"]//form//input[@id='${id}']`;;
                        // 如果id中包含rc_select，使用xpath
                        if (id.includes('rc_select')) {
                            xpath = `//div[@role='document']//div[@title='${name}']/ancestor::div[contains(@class,'ant-row ant-form-item')]//input`;
                        }
                        var placeholder = inputElement.placeholder || '';

                        // 拼装对象
                        var inputInfo = {
                            type: type,
                            index: index,
                            id: id,
                            placeholder: name ? name :placeholder,
                            xpath: xpath
                        };
                        inputInfoArray.push(inputInfo);
                    }
                }
            });
            // 返回所有 input 元素的信息数组
            return inputInfoArray;
        } else {
            console.log('当前页面未找到匹配的查询表单元素！');
            return null;
        }
    }  else if (element.tagName === 'MAIN') {
        // 假设 ancestorQueryList  ancestorQueryTable 已通过 closest 方法获取
        var ancestorQueryList = element.querySelector('div[class*="list-query-form"]') ? element.querySelector('div[class*="list-query-form"]').querySelector('form') : null;
        var ancestorQueryTable = element.querySelector('div[class*="list-table"]') ? element.querySelector('div[class*="list-table"]').querySelector('div[class="h-b-button-group-container"]') : null;

        // 步骤1：检查 ancestorQueryList 是否存在
        if (ancestorQueryList) {
            // 步骤2：获取所有下级 input 元素
            var inputElements = ancestorQueryList.querySelectorAll('input');
            var inputInfoArray = [];
            
            // 步骤3：遍历 input 元素（方法1：使用 forEach）
            inputElements.forEach(function(input, index) {
                // 对每个 input 元素执行操作，拼装对象
                var inputInfo = {
                    type: input.type,
                    index: index,
                    id: input.id,
                    placeholder: input.placeholder
                };
                inputInfoArray.push(inputInfo);
            });
            
            // 返回所有 input 元素的信息数组
            return inputInfoArray;

        } else {
            console.log('当前页面未找到匹配的查询表单元素！');
            return null;
        }
    } else {
        console.log('页面信息错误，请联系管理员（测试部）！');
        return null;
    }
}


// 通用处理函数
function handleElementAction(event, actionType) {
    if (!event || !event.target) {
        console.error("Invalid event object:", event);
        return;
    }
    // console.log(actionType === 'click' ? '点击事件' : actionType === 'double_click' ? '双击事件' : '右键事件');
    var element = event.target;
    var action = actionType === 'click' ? 'click' : actionType === 'double_click' ? 'double_click' : 'click_right';
    var operationText = '';
    var xpath = '';
    var attributes = {};


    if (element) {
        xpath_text = getXpathWithText(element);
        xpath = xpath_text['xpath'];
        operationText = xpath_text['operationText'];
        if (xpath) {
            console.log(xpath);
            logs.push({
                validate: isLocatorUnique(xpath),
                action: action,
                xpath: xpath,
                operationText: operationText,
                attributes: attributes
            });
        }
    }
}

// 辅助函数保持不变
function getTextContent(element) {
    var textContent = '';
    if (element.textContent) {
        return element.textContent.trim();
    }
    Array.from(element.childNodes).forEach(function(node) {
        if (node.nodeType === Node.TEXT_NODE) { // 只处理文本节点
            textContent += node.nodeValue.trim(); // 拼接文本内容并去除首尾空格
            console.log(textContent)
        }
    });
    return textContent;
}

function getTdSelect(element) {
    try{
//        const targetTd = Array.from(element.parentElement.parentElement.children).find(el => el.getAttribute('data-name') === 'ENAME' || el.getAttribute('data-name') === 'ECODE' || el.getAttribute('nowidth') === 'N');
        const targetTd = Array.from(element.parentElement.parentElement.children).find(el => {
          const nameAttr = el.getAttribute('data-name');
          return (nameAttr && (nameAttr === 'ENAME' || nameAttr === 'ECODE'));
        }) || Array.from(element.parentElement.parentElement.children).find(el => {
          const nowidthAttr = el.getAttribute('nowidth');
          return (nowidthAttr && nowidthAttr === 'N');
        })
        var tdIMG = element.parentElement.nextElementSibling;
        if (targetTd) {
            if (tdIMG) {
                var type_text = tdIMG.getAttribute('title').trim();
            } else {
                type_text = '';
            }
            // 获取并去除多余空白
            const tdText = targetTd.getAttribute('title');
            if (!tdText) return null;
            const hasDataName = targetTd.hasAttribute('data-name');
            if (tdText.includes('/')) {
                const prefix = tdText.split('/')[0];
                return hasDataName
                  ? [type_text, `//td[contains(@title, '${prefix}')]/preceding-sibling::td/span`, prefix]
                  : [type_text, `//td[contains(@title, '${prefix}')]/following-sibling::td/span`, prefix];
            } else {
              return hasDataName
                ? [type_text, `//td[@title='${tdText}']/preceding-sibling::td/span`, tdText]
                : [type_text, `//td[@title='${tdText}']/following-sibling::td/span`, tdText];
            }
        } else {
            return null;
        }
    } catch (error) {
        return null;
    }
}

function getTdIMG(element) {
    const targetTd = Array.from(element.parentElement.parentElement.children).find(el => el.getAttribute('data-name') === 'ENAME' || el.getAttribute('data-name') === 'ECODE');
    var tdIMG = element.parentElement.nextElementSibling;
    if (targetTd) {
        var type_text = tdIMG.getAttribute('title').trim();
        var tdText = targetTd.getAttribute('title'); // 获取并去除多余空白
        return [type_text + tdText + '的图标', tdText];
    }
    return null;
}

function getInputLabel(element) {
    // 从父节点开始查找最近的祖父级
    const ancestorTab = element.parentElement?.closest('div[role="document"]');
    const ancestorForm = element.parentElement?.closest('form[class*="ant-form"]');
    // 提前返回条件判断
    if (!ancestorTab && !ancestorForm) return null;

    let parentDiv = ancestorTab ?? ancestorForm ?? null;

    if (parentDiv && parentDiv.parentElement.previousElementSibling) {
        var titleDiv = parentDiv.querySelector('label').querySelector('div');
        if (titleDiv) {
            return titleDiv.getAttribute("title");
        }
    }
    return '输入框';
}

function getPreElement(currentNode) {
  // 获取所有兄弟节点（包括非相邻的）
  const siblings = Array.from(currentNode.parentNode.children)
    .filter(sibling => sibling !== currentNode);

  // 遍历兄弟节点寻找符合条件的第一个
  for (const sibling of siblings) {
    const title = sibling.getAttribute('title') || '';
    const dataName = sibling.getAttribute('data-name');

    if(dataName === 'ENAME' || dataName === 'ECODE') {
      let relation = '';
      // 检查sibling是否在currentNode之前
      if (sibling.compareDocumentPosition(currentNode) & Node.DOCUMENT_POSITION_PRECEDING) {
        relation = '/preceding-sibling::';
      } else if (sibling.compareDocumentPosition(currentNode) & Node.DOCUMENT_POSITION_FOLLOWING) {
        relation = '/following-sibling::';
      }

      if (title.includes('/')) {
        const cleanTitle = title.split('/')[0];
        return `//td[contains(@title,'${cleanTitle}')]${relation}`;
      } else {
        return `//td[@title='${title}']${relation}`;
      }
    }
  }
  return null; // 没有匹配时返回空字符串
}

function getBomIndex(currentNode) {
    // 向前查找最近的一个tr并且包含data-index的节点
    const trNode = currentNode.closest('tr[data-index]');
    if (trNode) {
        index = trNode.getAttribute('data-index');
        // 向前查找最近的一个td并且包含data-name的节点
        const tdNode = currentNode.closest('td[data-name]');
        if (tdNode) {
            const dataName = tdNode.getAttribute('data-name');
            return `//td[@title='${index}']/following-sibling::td[@data-name='${dataName}']`;
        } else {
            return `//td[@title='${index}']/following-sibling::td`;
        }

    }
    return null;
}

function getAncestorWithTabidXPath (element) {
    // 从父节点开始查找最近的祖父级 div[tabid]
    const ancestorTab = element.parentElement?.closest('div[role="document"]');
    const ancestorForm = element.parentElement?.closest('form[class*="ant-form"]');
    // 提前返回条件判断
    if (!ancestorTab && !ancestorForm) return null;

    let ancestor = ancestorTab ?? ancestorForm ?? null;
    console.log('找到的祖先元素:', ancestor);

    const lableNode = ancestor.querySelector('label').querySelector('div');
    const lableTitle= lableNode?.getAttribute('title');
    if (!lableTitle) return null;

    const nodeId = ancestor.tagName;

    // 查找包含特定class的祖先节点
    const targetNode = ancestor.querySelector('input');
    const targetId = targetNode?.getAttribute('id');
    if (!targetId) return null;

    // 组合最终XPath
    return nodeId.toLowerCase() === 'div'
        ? `//div[@role='document']//div[@title='${lableTitle}']/ancestor::input[@id=${targetId}]`
        : nodeId.toLowerCase() === 'form'
        ? `//form[contains(@class, "ant-form")]//div[@title='${lableTitle}']/ancestor::input[@id=${targetId}]`
        : null;
}

function getAncestorDialogXPath(element) {
    const ancestorDialog = element.parentElement?.closest(`div[role='dialog']`);
    return ancestorDialog ? `//div[@role='dialog']` : null;
}

function getAncestorWithCidXPath(element) {
    const ancestorCid = element.parentElement?.closest('div[cid]');
    if (ancestorCid) {
        return `//div[@cid='${ancestorCid.getAttribute('cid')}']`;
    }
    return null;
}




function getXpathWithText(element) {
    console.log(element.tagName)
    var xpath = '';
    var operationText = '';
    if (element.tagName === 'BUTTON') {
        var ancestorDialog = getAncestorDialogXPath(element);
        if (ancestorDialog) {
            if (element.hasAttribute('value')) {
                xpath = `${ancestorDialog}//button[@value='${element.getAttribute('value')}']`;
                operationText = element.getAttribute('value');
            } else if (element.hasAttribute('title')) {
                xpath = `${ancestorDialog}//button[@title='${element.getAttribute('title')}']`;
                operationText = element.getAttribute('title');
            }
        } else {
            if (element.hasAttribute('value')) {
                xpath = `//button[@value='${element.getAttribute('value')}']`;
                operationText = element.getAttribute('value');
            } else if (element.hasAttribute('title')) {
                xpath = `//button[@title='${element.getAttribute('title')}']`;
                operationText = element.getAttribute('title');
            }
        }

    } else if (element.tagName === 'SPAN') {
        var ancestorTabid = getAncestorWithTabidXPath(element);
        var ancestorDialog = getAncestorDialogXPath(element);
        var tdSelect = getTdSelect(element);
        var ancestorTd = element.closest('td') || ancestorTdNode;
        var ancestorLi = element.closest('li');
        var indexXpath = getBomIndex(element)
        if (ancestorTabid) {
            if (tdSelect) {
                xpath = `${ancestorTabid}${tdSelect[1]}`;
                operationText = '【'+ tdSelect[0] + '】' +tdSelect[2];
            } else if (element.hasAttribute('title') && element.getAttribute('title').length > 0 && !ancestorTabid.includes('BOM')) {
                xpath = `${ancestorTabid}//span[@title='${element.getAttribute('title')}']`;
                operationText = element.getAttribute('title');
            } else if (element.textContent.includes(' (')) {
                xpath = `${ancestorTabid}//span[contains(text(), '${element.textContent.split(' (')[0]}')]`;
                operationText = '左侧树节点：' + element.textContent.split(' (')[0];
            } else if (element.textContent.includes('(')) {
                xpath = `${ancestorTabid}//span[contains(text(), '${element.textContent.split('(')[0]}')]`;
                operationText = '左侧树节点：' + element.textContent.split('(')[0];
            } else if(element.textContent){
                if (indexXpath) {
                    xpath = `${ancestorTabid}${indexXpath}//span[text()='${element.textContent}']`;
                } else {
                    xpath = `${ancestorTabid}//span[text()='${element.textContent}']`;
                }
                operationText = getTextContent(element);
            } else if (ancestorLi && ancestorLi.getAttribute('val') > 0 && element.textContent.length < 1) {
                xpath = `${ancestorTabid}//li[@val='${ancestorLi.getAttribute('val')}']`;
                var next_span = element.nextElementSibling;
                if (next_span && next_span.textContent.length > 0) {
                    operationText = next_span.textContent;
                } else {
                    operationText = ancestorLi.getAttribute('val');
                }
            } else if (element.getAttribute('class')) {
                operationText = element.getAttribute('class');
                 if (indexXpath) {
                    xpath = `${ancestorTabid}${indexXpath}//span[@class='${element.getAttribute('class')}']`;
                } else {
                    xpath = `${ancestorTabid}//span[@class='${element.getAttribute('class')}']`;
                }
            }
        } else if(ancestorDialog) {
            if (tdSelect) {
                xpath = `${ancestorDialog}${tdSelect[1]}`;
                operationText = '【'+ tdSelect[0] + '】' +tdSelect[2];
            } else if (ancestorTd && ancestorTd.hasAttribute('data-name')) {
                var dataName = ancestorTd.getAttribute('data-name');
                var rownumSiblings = ancestorTd.parentNode.getElementsByTagName('td');
                var index = '';
                for (var i = 0; i < rownumSiblings.length; i++) {
                    if (rownumSiblings[i].getAttribute('rownum')) {
                        index = rownumSiblings[i].getAttribute('title');
                        break;
                    }
                }
                if (index) {
                    xpath = "//div[@role='dialog']//td[@title='" + index + "']/following-sibling::td[@data-name='" + dataName + "']//span";
                    operationText = '${index}${dataName}列';
                } else {
                    xpath = `//div[@role='dialog']//td[@data-name='${ancestorTd.getAttribute('data-name')}']//span`;
                    operationText = ancestorTd.getAttribute('data-name');
                }
            } else if (element.getAttribute('class') && element.getAttribute('class').includes('close')) {
                xpath = `//div[@role='dialog']//span[contains(@class, 'b-dialog-close')]`;
                operationText = '弹窗右上角关闭';
            } else if (element.textContent.length > 0) {
                xpath = `${ancestorDialog}//span[text()='${element.textContent}']`;
                operationText = element.textContent;
            } else if (element.getAttribute('class')) {
                xpath = `//div[@role='dialog']//span[@class='${element.getAttribute('class')}']`;
                operationText = element.getAttribute('class');
            } else if(element.getAttribute('title') && element.getAttribute('title').length > 0) {
                xpath = `//div[@role='dialog']//span[@title='${element.getAttribute('title')}']`;
                operationText = element.getAttribute('title');
            } else if (element.closest('td').hasAttribute('data-name')) {
                var ancestorTd = element.closest('td');
                var dataName = ancestorTd.getAttribute('data-name');
                var rownumSiblings = ancestorTd.parentNode.getElementsByTagName('td');
                var index = '';
                for (var i = 0; i < rownumSiblings.length; i++) {
                    if (rownumSiblings[i].getAttribute('rownum')) {
                        index = rownumSiblings[i].getAttribute('title');
                        break;
                    }
                }
                xpath = "//div[@role='dialog']//td[@title='" + index + "']/following-sibling::td[@data-name='" + dataName + "']//span";
                operationText = '${index}${dataName}列';
            }
        } else if(ancestorLi) {
            if (ancestorLi && ancestorLi.hasAttribute('val')) {
                xpath = `//li[@val='${ancestorLi.getAttribute('val')}']//span[text()='${element.textContent}']`;
                operationText = element.textContent;
            } else if (ancestorLi && ancestorLi.hasAttribute('navname')) {
                if(ancestorDialog) {
                    xpath = `${ancestorDialog}//span[@title='${element.textContent}']`;
                    operationText = element.textContent;
                } else {
                    if(element.hasAttribute('title')){
                        xpath = `//div[@class='head']//span[@title='${element.textContent}']`;
                        operationText = '顶部导航' + element.textContent;
                    } else {
                        var pre_span = element.previousElementSibling;
                        operationText = '顶部导航' + pre_span.textContent + '的关闭按钮';
                        xpath = `//div[@class='head']//span[@title='${pre_span.textContent}']/following-sibling::span`;
                    }
                }
            } else if (element.textContent.length > 0) {
                if (element.textContent.includes('权限')) {
                    xpath = `//span[contains(text(), '${element.textContent.split('的')[1]}')]`;
                } else if (element.textContent.includes('...')) {
                    xpath = `//span[contains(text(), '${element.textContent.split('...')[0]}')]`;
                } else {
                    xpath = `//span[text()='${element.textContent}']`;
                }
                operationText = element.textContent;
            }
        } else if(element.getAttribute('title') && element.getAttribute('title').length > 0) {
            xpath = `//span[@title='${element.getAttribute('title')}']`;
            operationText = element.getAttribute('title');
        } else if (element.getAttribute('class').includes('close')) {
            xpath = `//span[contains(@class, 'b-dialog-close')]`;
            operationText = '关闭';
        } else if (element.textContent.length > 0) {
            xpath = `//span[text()='${element.textContent}']`;
            operationText = element.textContent;
        } else if (ancestorTd && ancestorTd.hasAttribute('data-name')) {
            var dataName = ancestorTd.getAttribute('data-name');
            var rownumSiblings = ancestorTd.parentNode.getElementsByTagName('td');
            var index = '';
            for (var i = 0; i < rownumSiblings.length; i++) {
                if (rownumSiblings[i].getAttribute('rownum')) {
                    index = rownumSiblings[i].getAttribute('title');
                    break;
                }
            }
            if (index) {
                xpath = "//div[@role='dialog']//td[@title='" + index + "']/following-sibling::td[@data-name='" + dataName + "']//span";
                operationText = '${index}${dataName}列';
            } else {
                xpath = `//div[@role='dialog']//td[@data-name='${ancestorTd.getAttribute('data-name')}']//span`;
                operationText = ancestorTd.getAttribute('data-name');
            }
        } else if (element.getAttribute('class')) {
            xpath = `//span[@class='${element.getAttribute('class')}']`;
            operationText = element.getAttribute('class');
        }
    }  else if (element.tagName === 'A') {
        var ancestorTabid = getAncestorWithTabidXPath(element);
        var ancestorDialog = getAncestorDialogXPath(element);
        var ancestorLi = element.closest('li');
        if (ancestorTabid) {
            if (element.hasAttribute('title') && element.getAttribute('title').length > 0) {
                xpath = `${ancestorTabid}//a[@title='${element.getAttribute('title')}']`;
                operationText = element.getAttribute('title');
            } else {
                operationText = element.textContent.split('/')[0];
                if (element.textContent.includes('/')) {
                    xpath = `${ancestorTabid}//a[contains(text(), '${element.textContent.split('/')[0]}')]`;
                } else {
                    xpath = `${ancestorTabid}//a[text()='${element.textContent}']`;
                }
            }
        } else if (ancestorLi && ancestorLi.hasAttribute('val')) {
            if (ancestorLi.hasAttribute('objtype')) {
                xpath = `//li[@objtype='${ancestorLi.getAttribute('objtype')}' and @val='${ancestorLi.getAttribute('val')}']//a`;
            } else {
                xpath = `//li[@val='${ancestorLi.getAttribute('val')}']//a`;
            }
            operationText = getTextContent(element);
        }  else if(ancestorDialog) {
            if (element.hasAttribute('title') && element.getAttribute('title').length > 0) {
                xpath = `${ancestorDialog}//a[text()='${element.getAttribute('title')}']`;
                operationText = element.getAttribute('title');
            } else if (element.textContent.length > 0) {
                xpath = `${ancestorDialog}//a[text()='${element.textContent}']`;
                operationText = element.textContent;
            }
        } else if (element.hasAttribute('title') && element.getAttribute('title').length > 0) {
            xpath = `//a[@title='${element.getAttribute('title')}']`;
            operationText = element.getAttribute('title');
        } else if (element.textContent.length > 0) {
            xpath = `//a[text()='${element.textContent}']`;
            operationText = element.textContent;
        }
    }  else if (element.tagName === 'TH') {
        xpath = `//div[contains(@style,'display: block')]//th[text()='${element.textContent}']`;
        operationText = element.textContent;
    }  else if (element.tagName === 'SELECT') {
        var ancestorTd = element.closest('td');
        var ancestorDialog = getAncestorDialogXPath(element);
        var dataName = ancestorTd.getAttribute('data-name');
        var rownumSiblings = ancestorTd.parentNode.getElementsByTagName('td');
        var targetTitle = '';
        for (var i = 0; i < rownumSiblings.length; i++) {
            if (rownumSiblings[i].getAttribute('rownum')) {
                targetTitle = rownumSiblings[i].getAttribute('title');
                break;
            }
        }
        if (ancestorDialog) {
            xpath = "//div[@role='dialog']//td[@title='" + targetTitle + "']/following-sibling::td[@data-name='" + dataName + "']//select";
        }
        operationText = '下拉选择框';
    }  else if (element.tagName === 'OPTION') {
        if (element.hasAttribute('title') && element.getAttribute('title').length > 0) {
            xpath = `//option[@title='${element.getAttribute('title')}']`;
            operationText = element.getAttribute('title');
        } else if (element.hasAttribute('value') && element.getAttribute('value').length > 0) {
            xpath = `//option[@value='${element.getAttribute('value')}']`;
            operationText = element.getAttribute('value');
        } else {
            xpath = `//option[text()='${element.textContent}']`;
            operationText = element.textContent;
        }
    }  else if (element.tagName === 'TD') {
        var ancestorTabid = getAncestorWithTabidXPath(element);
        var ancestorDialog = getAncestorDialogXPath(element);
        if (ancestorTabid) {
            if (element.hasAttribute('title') && element.getAttribute('title').length > 0) {
                operationText = element.getAttribute('title').split('/')[0];
                var pre_ele_xpath = getPreElement(element);
                if (element.getAttribute('title').includes('/')) {
                    if (pre_ele_xpath) {
                        xpath = `${ancestorTabid}${pre_ele_xpath}td[contains(@title, '${element.getAttribute('title').split('/')[0]}')]`;
                    } else {
                        xpath = `${ancestorTabid}//td[contains(@title, '${element.getAttribute('title').split('/')[0]}')]`;
                    }

                } else {
                    if (pre_ele_xpath) {
                        xpath = `${ancestorTabid}${pre_ele_xpath}td[@title='${element.getAttribute('title')}' and @data-name='${element.getAttribute('data-name')}']`;
                    } else {
                        xpath = `${ancestorTabid}//td[@title='${element.getAttribute('title')}']`;
                    }
                }
            } else if (element.hasAttribute('data-name') && element.getAttribute('data-name').length > 0) {
                xpath = `${ancestorTabid}//td[@data-name='${element.getAttribute('data-name')}']`;
                operationText = element.getAttribute('data-name');
            } else if (element.hasAttribute('data-colname') && element.getAttribute('data-colname').length > 0) {
                const text = getTextContent(element);
                if (text) {
                    xpath = `${ancestorTabid}//td[@data-colname='${element.getAttribute('data-colname')}' and text()='${text}']`;
                    operationText = text;
                } else {
                    xpath = `${ancestorTabid}//td[@data-colname='${element.getAttribute('data-colname')}']`;
                    operationText = element.getAttribute('data-name');
                }
            } else if (element.textContent.length > 0) {
                operationText = element.textContent.split('/')[0];
                if (element.textContent.includes('/')) {
                    xpath = `${ancestorTabid}//td[contains(text(), '${element.textContent.split('/')[0]}')]`;
                } else {
                    xpath = `${ancestorTabid}//td[text()='${element.textContent}']`;
                }
            }
        } else if (ancestorDialog) {
            if (element.getAttribute('title').length > 0) {
                xpath = `${ancestorDialog}//td[@title='${element.getAttribute('title')}']`;
                operationText = element.getAttribute('title');
            } else if (element.getAttribute('data-name').length > 0) {
                operationText = element.getAttribute('data-name');
                var rownumSiblings = element.parentNode.getElementsByTagName('td');
                var targetTitle = '';
                for (var i = 0; i < rownumSiblings.length; i++) {
                    if (rownumSiblings[i].getAttribute('rownum')) {
                        targetTitle = rownumSiblings[i].getAttribute('title');
                        break;
                    }
                }
                if (targetTitle.length > 0) {
                    xpath = "//div[@role='dialog']//td[@title='" + targetTitle + "']/following-sibling::td[@data-name='" + operationText + "']";
                } else {
                    xpath = `${ancestorDialog}//td[@data-name='${element.getAttribute('data-name')}']`;
                }
            } else if (element.textContent.length > 0) {
                xpath = `${ancestorDialog}//td[text()='${element.textContent}']`;
                operationText = element.textContent;
            }
        } else {
            xpath = `//div[contains(@style,'display: block')]//td[text()='${element.textContent}']`;
            operationText = element.textContent;
        }
    } else if (element.tagName === 'P') {
        xpath = `//p[text()='${element.textContent}']`;
        operationText = element.textContent
    } else if (element.tagName === 'IMG') {
        var ancestorTabid = getAncestorWithTabidXPath(element);
        var project = element.closest("td[data-colname='Name']");
        if (project) {
            text = getTextContent(project);
            xpath = `${ancestorTabid}//td[text()='${text}']/img`;
            operationText = '展开' + text
        } else {
            project = element.parentElement.parentElement.querySelector('td[data-colname="Name"]');
            if (project) {
                text = getTextContent(project);
                xpath = `${ancestorTabid}//td[text()='${text}']/preceding-sibling::td[@data-colname='${element.parentElement.getAttribute('data-colname')}']/img`;
                operationText = text + '的图标'
            }
        }
    } else if (element.tagName === 'DIV') {
        var ancestorTabid = getAncestorWithTabidXPath(element);
        var ancestorDialog = getAncestorDialogXPath(element);
        var ancestorLi = element.closest('li');
        var ancestorTd = element.closest('td');
        if (ancestorLi && ancestorLi.hasAttribute('name')) {
            xpath = `//li[@name='${ancestorLi.getAttribute('name')}']//div[@title='${element.textContent}']`;
            operationText = element.textContent;
        } else if (ancestorTd && ancestorTd.getAttribute('data-name') === 'IMGICONTYPE') {
            if (ancestorTabid){
                var result = getTdIMG(element);
                xpath = `${ancestorTabid}//td[contains(@title, '${result[1].split('/')[0]}')]/preceding-sibling::td[@data-name='IMGICONTYPE']/div`;
                operationText = result[0];
            } else if (ancestorDialog){
                var result = getTdIMG(element);
                xpath = `${ancestorDialog}//td[contains(@title, '${result[1].split('/')[0]}')]/preceding-sibling::td[@data-name='IMGICONTYPE']/div`;
                operationText = result[0];
            }
        } else if (ancestorTabid) {
            if (element.hasAttribute('data-name')) {
                xpath = `${ancestorTabid}//div[@title='${element.getAttribute('title')}']`;
                operationText = element.getAttribute('title');
            } else if(element.textContent){
                xpath = `${ancestorTabid}//div[text()='${element.textContent}']`;
                operationText = element.textContent;
            }
        } else if (element.hasAttribute('title') && element.getAttribute('title').length > 0) {
            if (ancestorTabid) {
                xpath = `${ancestorTabid}//div[@title='${element.getAttribute('title')}']`;
                operationText = element.getAttribute('title');
            } else if (ancestorDialog) {
                xpath = `${ancestorDialog}//div[@title='${element.getAttribute('title')}']`;
                operationText = element.getAttribute('title');
           } else {
                xpath = `//div[@title='${element.getAttribute('title')}']`;
                operationText = element.getAttribute('title');
           }
        } else if (element.getAttribute('class')) {
            if(element.getAttribute('class').includes('htgrid-td-changed')){
                var parentDataName = currentParentNode.getAttribute('data-name');
                var rownumSiblings = currentParentNode.parentNode.getElementsByTagName('td');
                var targetTitle = '';
                for (var i = 0; i < rownumSiblings.length; i++) {
                    if (rownumSiblings[i].getAttribute('rownum')) {
                        targetTitle = rownumSiblings[i].getAttribute('title');
                        break;
                    }
                }

                if (ancestorDialog) {
                    xpath = "//div[@role='dialog']//td[@title='" + targetTitle + "']/following-sibling::td[@data-name='" + parentDataName + "']/div";
                } else {
                    xpath = "//td[@title='" + targetTitle + "']/following-sibling::td[@data-name='" + parentDataName + "']/div";
                }
                operationText = parentDataName;
            } else if (ancestorTabid) {
                xpath = `${ancestorTabid}//div[@class='${element.getAttribute('class')}']`;
                operationText = element.getAttribute('class');
            } else if (ancestorDialog) {
                xpath = `${ancestorDialog}//div[@class='${element.getAttribute('class')}']`;
                operationText = element.getAttribute('class');
            } else {
                xpath = `//div[@class='${element.getAttribute('class')}']`;
                operationText = element.getAttribute('class');
            }
        }
    } else if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
        var ancestorTabid = getAncestorWithTabidXPath(element);
        var ancestorDialog = getAncestorDialogXPath(element);
        var ancestorCid = getAncestorWithCidXPath(element);
        if (ancestorTabid) {
            if (ancestorCid) {
                xpath = `${ancestorTabid}${ancestorCid}//${element.tagName.toLowerCase()}`;
                operationText = getInputLabel(element);
            } else {
                xpath = `${ancestorTabid}//${element.tagName.toLowerCase()}[@class='${element.getAttribute('class')}']`;
                operationText = '输入框';
            }
        } else if(ancestorDialog) {
            if (ancestorCid) {
                xpath = `//div[@role='dialog']${ancestorCid}//${element.tagName.toLowerCase()}`;
                operationText = getInputLabel(element);
                if (element.hasAttribute('value') && element.getAttribute('value').length > 0){
                    xpath = `//div[@role='dialog']${ancestorCid}//${element.tagName.toLowerCase()}[@value='${element.getAttribute('value')}']`;
                    operationText = element.getAttribute('value');
                }
            } else if (element.hasAttribute('value') && element.getAttribute('value').length > 0){
                xpath = `${ancestorDialog}//${element.tagName.toLowerCase()}[@value='${element.getAttribute('value')}']`;
                operationText = element.getAttribute('value');
            }
        } else {
            xpath = `//input[@class='${element.getAttribute('class')}']`;
            operationText = '输入框';
        }
    } else if (element.tagName === 'LI') {
        if (element.hasAttribute('val')) {
            xpath = `//li[@val='${element.getAttribute('val')}']`;
            operationText = element.getAttribute('val');
        } else if (element.hasAttribute('title')) {
            const ancestorUL = element.closest("ul[style*='display: none']");
            if (ancestorUL) {
                xpath = `//ul[contains(@style, 'display: block')]//li[@title='${element.getAttribute('title')}']`;
            } else {
                xpath = `//li[@title='${element.getAttribute('title')}']`;
            }
            operationText = element.getAttribute('title');
        }
    }
    return { xpath, operationText };
}

async function handleDynamicReadonlyInput(page) {
    const selector = "//input[@placeholder='请输入账号']";

    // 方案1：等待 readonly 属性消失
    try {
        await page.waitForFunction(
            selector => {
                const el = document.evaluate(
                    selector,
                    document,
                    null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE,
                    null
                ).singleNodeValue;
                return el && !el.hasAttribute('readonly');
            },
            selector,
            { timeout: 10000 } // 等待10秒
        );

        await page.locator(selector).fill('admin');
    } catch (error) {
        console.log('等待超时，尝试强制移除 readonly...');

        // 方案2：强制移除并填充
        await page.locator(selector).evaluate(el => {
            el.removeAttribute('readonly');
            el.value = 'admin';
            el.dispatchEvent(new Event('input', { bubbles: true }));
        });
    }
}


// 记录操作的JavaScript代码
const recording_script = `
// 获取所有DOM元素
function getAllElements() {
    const allElements = document.querySelectorAll('*');
    const elementsInfo = [];

    allElements.forEach((element, index) => {
        // 跳过document和window
        if (element === document || element === window) return;

        // 获取元素基本信息
        const info = {
            index: index,
            tagName: element.tagName,
            id: element.id,
            className: element.className,
            nodeType: element.nodeType,
            nodeName: element.nodeName,
            textContent: element.textContent?.substring(0, 100) || '', // 限制长度
            childNodesCount: element.childNodes.length,
            attributes: {}
        };

        // 获取所有属性
        if (element.attributes) {
            for (let attr of element.attributes) {
                info.attributes[attr.name] = attr.value;
            }
        }

        // 检查是否可见
        const style = window.getComputedStyle(element);
        info.isVisible = style.display !== 'none' &&
                        style.visibility !== 'hidden' &&
                        element.offsetWidth > 0 &&
                        element.offsetHeight > 0;

        // 获取位置信息
        const rect = element.getBoundingClientRect();
        info.boundingRect = {
            x: rect.x,
            y: rect.y,
            width: rect.width,
            height: rect.height,
            top: rect.top,
            right: rect.right,
            bottom: rect.bottom,
            left: rect.left
        };

        elementsInfo.push(info);
    });

    return elementsInfo;
}

// 打印元素信息
const allElements = getAllElements();
console.log('页面元素总数:', allElements.length);

// 分组打印
const elementCountByTag = {};
allElements.forEach(element => {
    const tag = element.tagName.toLowerCase();
    elementCountByTag[tag] = (elementCountByTag[tag] || 0) + 1;
});

console.log('按标签名统计:', elementCountByTag);

// 打印前20个元素详细信息
console.log('前20个元素详情:');
allElements.slice(0, 20).forEach(element => {
    console.log('[" + element.index + "] " + element.tagName + (element.id ? "#" + element.id : "") + (element.className ? "." + element.className : ""));
    console.log('  文本:', element.textContent);
    console.log('  可见:', element.isVisible);
    console.log('  大小:', element.boundingRect.width + 'x' + element.boundingRect.height);
    console.log('---');
});

// 返回所有元素供后续使用
return allElements;
`;
