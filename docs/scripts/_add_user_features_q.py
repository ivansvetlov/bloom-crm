# -*- coding: utf-8 -*-
from pathlib import Path

NEW_BLOCK = r'''
            <!-- БЛОК 10 -->
            <div class="wiz-block" data-block="10">
              <div class="wb-head"><span class="wb-num">10</span><span class="wb-title">Пользователи и функционал</span></div>
              <div class="wb-tag">блок 10/10 · кто работает · что нужно</div>

              <div class="wiz-item">
                <div class="wiz-q"><b>26.</b> Кто будет <b>основным пользователем</b> CRM в повседневной работе?</div>
                <div class="qopt-row" data-name="b10qUser" data-multi="true">
                  <label class="qopt"><input type="checkbox" name="b10qUser" value="portal"> Менеджеры портала / сети (центр, диспетчер)</label>
                  <label class="qopt"><input type="checkbox" name="b10qUser" value="shop"> Менеджеры магазинов (точки)</label>
                  <label class="qopt"><input type="checkbox" name="b10qUser" value="florist"> Флористы / сборка</label>
                  <label class="qopt"><input type="checkbox" name="b10qUser" value="owner"> Владелец / директор</label>
                  <label class="qopt"><input type="checkbox" name="b10qUser" value="partner"> Партнёрские точки</label>
                  <label class="qopt"><input type="checkbox" name="b10qUser" value="other"> Другое (напишите ниже)</label>
                </div>
                <textarea class="qfree" data-name="b10qUserNote" placeholder="Комментарий: кто главный, кто заходит реже…"></textarea>
              </div>

              <div class="wiz-item">
                <div class="wiz-q"><b>27.</b> <b>Нужный функционал</b> — отметьте, что важно в первой версии (уже заложено в демо-кабинете). Можно несколько.</div>
                <div class="qopt-row" data-name="b10qFeatures" data-multi="true">
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="orders_list"> Заказы: список и канбан</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="orders_status_pay"> Статус заказа + оплата + источник</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="orders_manual"> Ручной заказ (телефон, чат, витрина)</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="orders_card"> Карточка заказа (состав, адрес, лента)</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="chats"> Чаты: WhatsApp / Telegram / MAX в одном окне</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="chat_assign"> Назначение диалога на точку и менеджера</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="chat_templates"> Шаблоны ответов в чате</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="clients"> Клиенты: база, заказы клиента, сумма</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="tasks"> Задачи (сроки, исполнитель, связь с заказом)</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="notes"> Заметки</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="mail"> Почта (входящие / исходящие, связь с клиентом)</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="cases"> Обращения: жалобы, претензии, обратная связь</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="catalog"> Номенклатура (букеты, цены, остатки)</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="warehouses"> Склады: остатки по точкам, перемещения</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="invoices"> Счета (заказ → счёт → оплата)</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="reports"> Отчёты: продажи, каналы, точки, товары, операции, клиенты, качество</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="multishop"> Несколько магазинов, переключение точки</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="access"> Права доступа: роли, ACL, админка</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="marketplace"> Связка с маркетплейсом (заказы, статусы, каталог)</label>
                  <label class="qopt"><input type="checkbox" name="b10qFeatures" value="other"> Другое / отдельно (напишите ниже)</label>
                </div>
                <textarea class="qfree" data-name="b10qFeaturesNote" placeholder="Что критично в v1, что можно во вторую очередь…"></textarea>
              </div>
            </div>

'''

MD_BLOCK = """
## Блок 10 · Пользователи и функционал

26. **Основной пользователь CRM:** менеджеры портала / сети, менеджеры магазинов, флористы, владелец, партнёры (можно несколько)  
27. **Нужный функционал** (чек-лист по уже заложенному в демо + комментарий):  
    - заказы (список/канбан, статус+оплата+источник, ручной заказ, карточка)  
    - чаты (WA/TG/MAX, назначение на точку/менеджера, шаблоны)  
    - клиенты, задачи, заметки  
    - почта, обращения (жалобы/претензии)  
    - номенклатура, склады, счета  
    - отчёты (сводка / продажи / каналы / точки / товары / операции / клиенты / качество)  
    - мульти-магазин, права доступа, маркетплейс  
"""

html_files = list(Path(r"C:\Workspace\projects\flowwow-crm\docs").rglob("questions.html"))
md_files = list(Path(r"C:\Workspace\projects\flowwow-crm\docs").rglob("questions.md"))

for p in html_files:
    t = p.read_text(encoding="utf-8")
    if "b10qUser" in t:
        print("skip html", p)
        continue
    if "data-block=\"9\"" not in t and "data-block='9'" not in t:
        print("no block9", p)
        continue
    # insert before closing of form body (after block 9)
    needle = "            <!-- БЛОК 9 -->"
    # better: after last wiz-block of delivery, before </div> of wiz-body
    mark = '                <textarea class="qfree" data-name="b10q29" placeholder="Ваш ответ…"></textarea>\n              </div>\n            </div>\n\n          </div>'
    # actual data-name is b10q29 for question 25
    mark = 'data-name="b10q29"'
    idx = t.find(mark)
    if idx < 0:
        print("mark not found", p)
        continue
    # find end of block 9 after this
    end = t.find("            </div>\n\n          </div>", idx)
    if end < 0:
        end = t.find("</div>\n\n          </div>", idx)
    # find the closing of wiz-block 9 - after question 25's closing divs
    # structure: ... </div> item </div> block </div> body
    close_block = t.find("            </div>\n\n          </div>\n\n          <div class=\"contact-grid\"", idx)
    if close_block < 0:
        close_block = t.find('          <div class="contact-grid"', idx)
        # back up to insert before contact - need after block9 close
        # search backwards for block close
        insert_at = t.rfind("            </div>", idx, close_block)
        # include that closing of block9
        insert_at = t.find("\n", insert_at) + 1
    else:
        insert_at = close_block

    # Simpler approach: replace unique end of Q25 block
    old = '''              <div class="wiz-item">
                <div class="wiz-q"><b>25.</b> Нужно ли видеть, где находится курьер (трек-номер, карта), или достаточно ставить статус и отправлять клиенту сообщение «заказ в пути»?</div>
                <textarea class="qfree" data-name="b10q29" placeholder="Ваш ответ…"></textarea>
              </div>
            </div>

          </div>'''
    new = '''              <div class="wiz-item">
                <div class="wiz-q"><b>25.</b> Нужно ли видеть, где находится курьер (трек-номер, карта), или достаточно ставить статус и отправлять клиенту сообщение «заказ в пути»?</div>
                <textarea class="qfree" data-name="b10q29" placeholder="Ваш ответ…"></textarea>
              </div>
            </div>
''' + NEW_BLOCK + '''
          </div>'''
    if old not in t:
        print("old Q25 block not exact", p)
        # try loose
        if 'data-name="b10q29"' in t and "БЛОК 10" not in t:
            t = t.replace(
                '              </div>\n            </div>\n\n          </div>\n\n          <div class="contact-grid"',
                '              </div>\n            </div>\n' + NEW_BLOCK + '\n          </div>\n\n          <div class="contact-grid"',
                1,
            )
            # might match wrong place - only if one occurrence near end
            p.write_text(t, encoding="utf-8")
            print("loose insert", p)
        continue
    t = t.replace(old, new, 1)
    t = t.replace("Вопрос 1 из 25", "Вопрос 1 из 27")
    # update block tags 1/9 -> keep or update to 1/10
    t = t.replace("блок 1/9", "блок 1/10")
    t = t.replace("блок 2/9", "блок 2/10")
    t = t.replace("блок 3/9", "блок 3/10")
    t = t.replace("блок 4/9", "блок 4/10")
    t = t.replace("блок 5/9", "блок 5/10")
    t = t.replace("блок 6/9", "блок 6/10")
    t = t.replace("блок 7/9", "блок 7/10")
    t = t.replace("блок 8/9", "блок 8/10")
    t = t.replace("блок 9/9", "блок 9/10")
    p.write_text(t, encoding="utf-8")
    print("ok html", p)

for p in md_files:
    t = p.read_text(encoding="utf-8")
    if "Блок 10" in t or "b10qUser" in t or "Основной пользователь CRM" in t:
        print("skip md", p)
        continue
    t = t.replace("**25 вопросов · 9 блоков**", "**27 вопросов · 10 блоков**")
    t = t.replace("25 вопросов · 9 блоков", "27 вопросов · 10 блоков")
    if "## Блок 9 · Доставка" in t:
        t = t.replace(
            "## Блок 9 · Доставка\n\n24. Кто доставляет  \n25. Трек / карта или только статус  \n\n---",
            "## Блок 9 · Доставка\n\n24. Кто доставляет  \n25. Трек / карта или только статус  \n"
            + MD_BLOCK
            + "\n---",
        )
    else:
        t = t.rstrip() + "\n" + MD_BLOCK + "\n"
    p.write_text(t, encoding="utf-8")
    print("ok md", p)

print("done")
