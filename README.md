# �Զ���乤��ʹ��˵��
�Զ���乤����һ���app�����ж�Ӧ�������Զ����������еĲ�������json�ļ��н��ж��壬�� navicate-premium.json

���ĵ���Ҫ����������һ��app���������Զ���乤��ʵ��Ŀ�����

## ����app��ʵ���Զ����
���������navicat-premium���ߵ��Զ���������ӵ�mysql���ݿ�Ϊ��������ʵ�ֲ���

* ǰ������:
    - os: windows����ϵͳ
    - �Ѱ�װpython3��������python
    - navicat-premium�Ѱ�װ��������

* һ�������ӵ�navicat-premiumͼʾ����
    ![navicat-premium](images/navicat_connected.png)

### ��������

��cmd���������乤�ߴ�����ļ��С���f:/yyf_work_sta/cloudSoft-cpp/AppAutoFill

1. win + r ������cmd��cmd

2. ���� cd "f:/yyf_work_sta/cloudSoft-cpp/AppAutoFill"���س�,Ȼ�����f: ����Ŀ���ļ��� 

3. ����set APPLAUNCHER_DEBUG=1,��debug��Ϣ
    
### �����Զ�����json�ļ�
����ʵ����navicat�д����Ӳ��´���һ�����ӣ�������ӵ����ݿ�

* �����Ϣ����,��:Ϊ�ָ������ӵ�3�п�ʼ�����Ƿֱ���class id text,�����е��ĸ����ֱַ��ǲ��
  ���ϽǺ����꣬������ ���Ͻǵĺ�����������ꡣ
    ```bash
    13456:0x5f0960:TActionMainMenuBar:6228320:ActionMainMenuBar ->(0, 23, 1920, 50)
    ```
* ����ͨ�����Ҳ����Ϣ��ȷ�ϲ������󣬹������£�
    * ���id��ȷ�����ڶ�δ�ʱ���ֲ��䣬����ʹ��id
    * �����textֵ��ʹ��textֵ
    * �����classֵ��ʹ��classֵ
    * �������ֵ�ж������ʹ�ò���"seq"ȷ����Ҫѡȡ�Ĳ����seq��intֵ0Ϊ��һ����ֵ

* �Զ�����֧�ֶԲ������󣨴��ھ�����������в�����
    * keyboard����Ŀ������ͼ����¼���������ʽ����, ��һ��������ʾ��Ҫ���ڿؼ��ϵ���������λ�ã�[0,0]
    ��ʾ�������ꣻ�ڶ�������Ϊ������������ݣ�֧���ַ����Լ���Сд��������������ѡ��֧��CTRL��ALT
        ```bash
              {
                "desc": "�ÿ�ݼ������Ӵ���",
                "target": {},
                "event" : "keyboard",
                "param": [[0, 0], "u", "ctrl"],
                "wait": 2
              },
        ```
    * mouse: ��Ŀ�������������¼���������ʽ���£���һ��������ʶ�ڿؼ��ϵ���������λ�ã��ڶ���������ʾ
    �ǵ����������Ҽ���
        ```bash
              {
                "desc": "���OK��ť",
                "target": {
                  "text": "OK"
                },
                "event" : "mouse",
                "param": [[10, 10], "left"],
                "wait": 2
              },
        ```
    * message: ��Ŀ�������windows message�¼���һ��ΪWM_SETTEXT�������ı���Ϣ����һ������Ϊ��Ϣ���ͣ��ڶ�������
    Ϊ��Ϣ���ݡ�
        ```bash
              {
                "desc": "����IP��ַ",
                "target": {
                  "text": "127.0.0.1"
                },
                "event" : "message",
                "param": ["WM_SETTEXT", "192.168.4.40"],
                "wait": 0.1
              },
        ```
    * hide: ����Ŀ�����ͨ��Ϊ���뷨����
        ```bash
              {
                "desc": "�������뷨���˲������ʧ�ܣ�����ʧ�ܺ���Ȼ����",
                "target": {
                  "desc": "����ΪNativeHWNDHost�Ŀؼ�",
                  "class": "NativeHWNDHost",
                  "seq":0
                },
                "event": "hide",
                "param": [true],
                "wait": 0.1,
                "continue":true
              },
        ```

1. ���������ļ��������ļ�Ϊapp�����ɣ����ﴴ��navicate-premium.json�ļ�
    1. ������ǰtestĿ¼�µ�template.json����Ϊnavicate-premium.json
    2. ��ʵ���������ʾ�޸�navicate-premium.json�ļ��еĲ���������
        ```bash
           {
              "name": "navicate-premium",
              "path": "F:\\Navicat\\navicat.exe",
              "callback": "http://127.0.0.1:8080/callback",
              "autoFillInfo": {
                "title": "",
                "timeout": 10,
                "maximize": false,
                "action": [
                ]
              },
              "postrun": {
              }
           }
        ```
    3. ����һ���򵥵�web����������navicat.json copy���������£�web�������򵥵Ĵ�����[web_server_simulator.py](https://gitlab.cloudbility.cn:4443/cloudsoft/cloudSoft-cpp/blob/master/AppAutoFill/web_server_simulator.py)��������������ͬĿ¼����testĿ¼����navicate-premium.json���Ƶ�testĿ¼���ɡ�Ȼ��������������
    ```bash
    python3 web_server_simulator.py
    ```
   
2. ��������AppLauncher.exe����ȡ�����Ϣ������ʵ���������ݿ�Ĳ���
    1. ��cmd��ִ��ִ�� AppLauncher.exe http://127.0.0
    .1:8080/req?app=navicat-premium��app����ΪtestĿ¼��json��ǰ׺������Ὣnavicat�򿪲�����־�����������Ϣ
        ```bash
        find windows <win_app.win_app object at 0x04095FB0>(pid 13456, hwnd [<window_handler.window_handler object at 0x04367850>]) target {'text': '^Navicat'}
        dump all child window info
        13456:0x1100a86:TNavicatMainForm:0:Navicat Premium ->(-8, -8, 1928, 1048)
        13456:0x8e0ce4:TPanel:9309412: ->(1670, 114, 1920, 1018)
        13456:0x480484:TPanel:4719748: ->(1670, 139, 1920, 1018)
        13456:0x19063a:TNavicatSyncActivityLog:1639994: ->(1670, 139, 1920, 1018)
        13456:0x2a0160:TPanel:2752864:No object information available. ->(1670, 139, 1920, 1018)
        13456:0x30014e:TPanel:3146062: ->(1670, 114, 1920, 139)
        13456:0x480552:TPanel:4719954:PanelNSYUserInfo ->(1847, 23, 1920, 48)
        13456:0x5d0730:TPanel:6096688:plNSYSpace ->(1887, 23, 1895, 48)
        13456:0x48057e:TPanel:4719998: ->(0, 1018, 1920, 1040)
        13456:0x1e02c0:TStatusBar:1966784: ->(0, 1018, 1920, 1040)
        13456:0x5b0aaa:TPanel:5966506: ->(1869, 1019, 1919, 1040)
        13456:0x590c5a:TPanel:5835866: ->(1798, 1019, 1865, 1040)
        13456:0x3f084c:TPanel:4130892:PanelNavTabs ->(253, 114, 1667, 1018)
        13456:0xc0274:TPanel:787060: ->(253, 114, 1667, 144)
        13456:0x990cbe:TPanel:10030270: ->(253, 140, 1667, 144)
        13456:0x240c50:TNavicatRkSmartTabs:2362448: ->(253, 114, 1667, 140)
        13456:0x170ace:TPanel:1510094:PanelDockHost ->(253, 144, 1667, 1018)
        13456:0x29038a:TPanel:2687882: ->(253, 144, 1667, 1018)
        13456:0x2a0c94:TPanel:2755732: ->(253, 144, 1667, 170)
        13456:0x50070c:TPanel:5244684: ->(253, 144, 1638, 170)
        13456:0x3d081e:TActionToolBar:3999774:ActionToolBar2 ->(253, 144, 1638, 171)
        13456:0x3105a2:TPanel:3212706: ->(1638, 144, 1662, 170)
        13456:0x5d074a:TPanel:6096714: ->(253, 170, 1667, 1018)
        13456:0x450710:TPanel:4523792: ->(253, 170, 1667, 1018)
        13456:0x8506a2:TDiagramViewFrame:8717986: ->(253, 170, 807, 638)
        13456:0x2b05ae:TPanel:2819502: ->(253, 170, 807, 608)
        13456:0x2b0a36:TDDViewer:2820662: ->(253, 170, 807, 608)
        13456:0x59040a:TPanel:5833738: ->(253, 608, 807, 638)
        13456:0x3c041a:TPanel:3933210: ->(253, 608, 667, 638)
        13456:0x6b0a30:TActionToolBar:7014960:DiagramViewFrameToolBar ->(253, 611, 667, 638)
        13456:0xb5078e:TListView:11863950: ->(253, 170, 1667, 1018)
        13456:0x4205f0:TWinControlProxy:4326896: ->(253, 170, 253, 170)
        13456:0x3d0a0a:TActionToolBar:4000266:ActionToolBar ->(0, 50, 1920, 114)
        13456:0x5f0960:TActionMainMenuBar:6228320:ActionMainMenuBar ->(0, 23, 1920, 50)
        13456:0x290958:TPanel:2689368: ->(0, 114, 250, 1018)
        13456:0x330d02:TVTFilterFrame:3345666: ->(0, 114, 250, 1018)
        13456:0x1b0744:TVirtualStringTree:1771332: ->(0, 114, 250, 1018)
        13456:0x30065a:TWinControlProxy:3147354: ->(0, 114, 0, 114)
        Starting new HTTP connection (1): 127.0.0.1:8080
        http://127.0.0.1:8080 "GET /callback?success=true&msg= HTTP/1.1" 200 None
        Proc 13456 exits with code 0
        Exec post run for navicate-premium
        Starting new HTTP connection (1): 127.0.0.1:8080
        http://127.0.0.1:8080 "GET /callback?sessionClose=True HTTP/1.1" 200 None
        ```
    
    2. ������һ�������־��Ϣ���ҵ�**file**��Ӧ�Ĳ����ʵ������ƶ����˵����**File**��
        * ��������**file**��������Ͻǣ����Կ����������־���ų����ϽǺ��������Ĳ����
        * �����ܵĲ�����뵽��navicate-premium.json�е�action�У�
            * ��ֵ˵������
                - target: ȷ����Ҫ��ȡ�Ĳ��
                - event: ������Ϣ������꣬������Ϣ
                - param: ������ֵΪһ�����飬�����е�һ��ֵΪ������Ϊ���ƫ��������������ĵ��������
                ���event�Ƿ�����Ϣ����paramΪ������Ϣ����һ������Ϊ�������ڶ�������Ϊֵ
            * �ڳ��Զ�κ󣬼����������µ�aciton�п�ʵ�������**file**�˵���ע������Ҳ����ͨ�������������ҵ����
                ```bash
                    {
                    "target": {
                      "text": "ActionMainMenuBar"
                    },
                    "event": "mouse",
                    "param": [
                      [
                        10,
                        10
                      ],
                      "left"
                    ],
                    "wait": 0.5
                      }
                ```
            
    3. ��������1�е�exe���򣬻�ȡ���Ĳ����Ϣ����ȡ���µ���־��Ϣ������before exec��ִ�����������fileǰ�Ĳ����Ϣ��
    After exec ��ִ���������Ĳ����Ϣ����������Ӧ��ȥ�������Ĳ��
        ```bash
            ====================begin====================
            before exec action {'target': {'text': 'ActionMainMenuBar'}, 'event': 'mouse', 'param': [[10, 10], 'left'], 'wait': 0.5}
            find windows <win_app.win_app object at 0x0346B070>(pid 11576, hwnd [<window_handler.window_handler object at 0x037897F0>]) target {'text': 'ActionMainMenuBar'}
            dump all child window info
            11576:0x7b07c2:TNavicatMainForm:0:Navicat Premium ->(-8, -8, 1928, 1048)
            11576:0xbb0ad8:TPanel:12258008: ->(1670, 114, 1920, 1018)
            11576:0xc10ae2:TPanel:12651234: ->(1670, 139, 1920, 1018)
            11576:0x50b44:TNavicatSyncActivityLog:330564: ->(1670, 139, 1920, 1018)
            11576:0x320a38:TPanel:3279416:No object information available. ->(1670, 139, 1920, 1018)
            11576:0x2c0af0:TPanel:2886384: ->(1670, 114, 1920, 139)
            11576:0x1c0ae6:TPanel:1837798:PanelNSYUserInfo ->(1847, 23, 1920, 48)
            11576:0x210b3c:TPanel:2165564:plNSYSpace ->(1887, 23, 1895, 48)
            11576:0x6f0780:TPanel:7276416: ->(0, 1018, 1920, 1040)
            11576:0x2d05c4:TStatusBar:2950596: ->(0, 1018, 1920, 1040)
            11576:0x22607c0:TPanel:36046784: ->(1869, 1019, 1919, 1040)
            11576:0x3c0abe:TPanel:3934910: ->(1798, 1019, 1865, 1040)
            11576:0x530554:TPanel:5440852:PanelNavTabs ->(253, 114, 1667, 1018)
            11576:0x150b40:TPanel:1379136: ->(253, 114, 1667, 144)
            11576:0x1d0b66:TPanel:1903462: ->(253, 140, 1667, 144)
            11576:0x1e06bc:TNavicatRkSmartTabs:1967804: ->(253, 114, 1667, 140)
            11576:0x3804f0:TPanel:3671280:PanelDockHost ->(253, 144, 1667, 1018)
            11576:0x530ab8:TPanel:5442232: ->(253, 144, 1667, 1018)
            11576:0x300b20:TPanel:3148576: ->(253, 144, 1667, 170)
            11576:0x1305fe:TPanel:1246718: ->(253, 144, 1638, 170)
            11576:0x170b42:TActionToolBar:1510210:ActionToolBar2 ->(253, 144, 1638, 171)
            11576:0x3c057a:TPanel:3933562: ->(1638, 144, 1662, 170)
            11576:0x2a0066:TPanel:2752614: ->(253, 170, 1667, 1018)
            11576:0x90b78:TPanel:592760: ->(253, 170, 1667, 1018)
            11576:0x25064e:TDiagramViewFrame:2426446: ->(253, 170, 807, 638)
            11576:0x1d0692:TPanel:1902226: ->(253, 170, 807, 608)
            11576:0x1205e8:TDDViewer:1181160: ->(253, 170, 807, 608)
            11576:0x2805bc:TPanel:2622908: ->(253, 608, 807, 638)
            11576:0x9307b2:TPanel:9635762: ->(253, 608, 667, 638)
            11576:0x130682:TActionToolBar:1246850:DiagramViewFrameToolBar ->(253, 611, 667, 638)
            11576:0x380b14:TListView:3672852: ->(253, 170, 1667, 1018)
            11576:0x3d0820:TWinControlProxy:3999776: ->(253, 170, 253, 170)
            11576:0x410574:TActionToolBar:4261236:ActionToolBar ->(0, 50, 1920, 114)
            11576:0x3d0cee:TActionMainMenuBar:4001006:ActionMainMenuBar ->(0, 23, 1920, 50)
            11576:0x640be2:TPanel:6556642: ->(0, 114, 250, 1018)
            11576:0x170c2a:TVTFilterFrame:1510442: ->(0, 114, 250, 1018)
            11576:0x300a06:TVirtualStringTree:3148294: ->(0, 114, 250, 1018)
            11576:0x860ce2:TWinControlProxy:8785122: ->(0, 114, 0, 114)
            Post event mouse to 11576:0x3d0cee:TActionMainMenuBar:4001006:ActionMainMenuBar ->(0, 23, 1920, 50)
            Move mouse to (10,33)
            Click mouse with button LEFT
            After exec action {'target': {'text': 'ActionMainMenuBar'}, 'event': 'mouse', 'param': [[10, 10], 'left'], 'wait': 0.5}
            dump all child window info
            11576:0x5a06ae:TThemedPopupMenu:0: ->(1, 49, 191, 297)
            ====================end====================
        ```
    
    4. ���������ʵ������ƶ������ڲ���3��ִ�к�ֻ��1�������Ϣ������������action������������¡�
        ```bash
        {
                "target": {
                  "class": "TThemedPopupMenu"
                },
                "event": "mouse",
                "param": [
                  [
                    10,
                    30
                  ],
                  ""
                ],
                "wait": 0.5
        }
        ```
        
    5. �ظ�����3�Ͳ���4��һ��һ��ʵ�������������ݿ��Ŀ�ġ��õ���json�ļ���������
        ```bash
        {
          "name": "navicate-premium",
          "path": "F:\\Navicat\\navicat.exe",
          "callback": "http://127.0.0.1:8080/callback",
          "autoFillInfo": {
            "title": "^Navicat",
            "timeout": 10,
            "maximize": false,
            "action": [
              {
                "target": {
                  "text": "ActionMainMenuBar"
                },
                "event": "mouse",
                "param": [
                  [
                    10,
                    10
                  ],
                  "left"
                ],
                "wait": 0.5
              },
              {
                "target": {
                  "class": "TThemedPopupMenu"
                },
                "event": "mouse",
                "param": [
                  [
                    10,
                    30
                  ],
                  ""
                ],
                "wait": 0.5
              },
              {
                "target": {
                  "class": "TThemedPopupMenu"
                },
                "event": "mouse",
                "param": [
                  [
                    50,
                    10
                  ],
                  ""
                ],
                "wait": 0.5
              },
              {
                "target": {
                  "class": "TThemedPopupMenu"
                },
                "event": "mouse",
                "param": [
                  [
                    10,
                    10
                  ],
                  "left"
                ],
                "wait": 0.5
              },
              {
                "target": {
                  "class": "TEdit",
                  "seq": 4
                },
                "event": "message",
                "param": [
                  "WM_SETTEXT",
                  "scott_test"
                ]
              },
              {
                "target": {
                  "class": "TEdit",
                  "seq": 0
                },
                "event": "message",
                "param": [
                  "WM_SETTEXT",
                  "192.168.4.73"
                ]
              },
              {
                "target": {
                  "class": "TEdit",
                  "seq": 3
                },
                "event": "message",
                "param": [
                  "WM_SETTEXT",
                  "3306"
                ]
              },
              {
                "target": {
                  "class": "TEdit",
                  "seq": 2
                },
                "event": "message",
                "param": [
                  "WM_SETTEXT",
                  "root"
                ]
              },
              {
                "target": {
                  "class": "TEdit",
                  "seq": 1
                },
                "event": "message",
                "param": [
                  "WM_SETTEXT",
                  "sky123"
                ]
              },
              {
                "target": {
                  "class": "TButton",
                  "text": "OK"
                },
                "event": "mouse",
                "param": [
                  [
                    10,
                    10
                  ],
                  "left"
                ],
                "wait": 0.5
              },
              {
                "desc": "action",
                "target": {
                  "class": "TVirtualStringTree"
                },
                "event": "mouse",
                "param": [
                  [
                    20,
                    10
                  ],
                  "right"
                ],
                "wait": 1
              },
              {
                "target": {
                  "class": "#32768"
                },
                "event": "mouse",
                "param": [
                  [
                    20,
                    10
                  ],
                  "left"
                ],
                "wait": 1
              }
            ]
          },
          "postrun": [
            
              ]
        }
        ```
    
    6. ʵ�ֹر�app���������ӹ������������json�ļ���postrun�����ж��塣������ɾ��navicat�е����Ӵ��Ķ��壬���Թ��ο�
        ```bash
               {
                  "action": "fileclean",
                  "params": [
                    "%USERPROFILE%\\Documents\\Navicat"
                  ]
                },
                {
                  "action": "regclean",
                  "params": [
                    "HKEY_CURRENT_USER\\Software\\PremiumSoft\\Navicat\\Servers"
                  ]
                },
                {
                  "action": "command",
                  "params": [
                    "echo",
                    "test"
                  ]
                }
        ```
        
    7. ���յ�json�ļ���������
        ```bash
            {
              "name": "navicate-premium",
              "path": "F:\\Navicat\\navicat.exe",
              "callback": "http://127.0.0.1:8080/callback",
              "autoFillInfo": {
                "title": "^Navicat",
                "timeout": 10,
                "maximize": false,
                "action": [
                  {
                    "target": {
                      "text": "ActionMainMenuBar"
                    },
                    "event": "mouse",
                    "param": [
                      [
                        10,
                        10
                      ],
                      "left"
                    ],
                    "wait": 0.5
                  },
                  {
                    "target": {
                      "class": "TThemedPopupMenu"
                    },
                    "event": "mouse",
                    "param": [
                      [
                        10,
                        30
                      ],
                      ""
                    ],
                    "wait": 0.5
                  },
                  {
                    "target": {
                      "class": "TThemedPopupMenu"
                    },
                    "event": "mouse",
                    "param": [
                      [
                        50,
                        10
                      ],
                      ""
                    ],
                    "wait": 0.5
                  },
                  {
                    "target": {
                      "class": "TThemedPopupMenu"
                    },
                    "event": "mouse",
                    "param": [
                      [
                        10,
                        10
                      ],
                      "left"
                    ],
                    "wait": 0.5
                  },
                  {
                    "target": {
                      "class": "TEdit",
                      "seq": 4
                    },
                    "event": "message",
                    "param": [
                      "WM_SETTEXT",
                      "scott_test"
                    ]
                  },
                  {
                    "target": {
                      "class": "TEdit",
                      "seq": 0
                    },
                    "event": "message",
                    "param": [
                      "WM_SETTEXT",
                      "192.168.4.73"
                    ]
                  },
                  {
                    "target": {
                      "class": "TEdit",
                      "seq": 3
                    },
                    "event": "message",
                    "param": [
                      "WM_SETTEXT",
                      "3306"
                    ]
                  },
                  {
                    "target": {
                      "class": "TEdit",
                      "seq": 2
                    },
                    "event": "message",
                    "param": [
                      "WM_SETTEXT",
                      "root"
                    ]
                  },
                  {
                    "target": {
                      "class": "TEdit",
                      "seq": 1
                    },
                    "event": "message",
                    "param": [
                      "WM_SETTEXT",
                      "sky123"
                    ]
                  },
                  {
                    "target": {
                      "class": "TButton",
                      "text": "OK"
                    },
                    "event": "mouse",
                    "param": [
                      [
                        10,
                        10
                      ],
                      "left"
                    ],
                    "wait": 0.5
                  },
                  {
                    "desc": "action",
                    "target": {
                      "class": "TVirtualStringTree"
                    },
                    "event": "mouse",
                    "param": [
                      [
                        20,
                        10
                      ],
                      "right"
                    ],
                    "wait": 1
                  },
                  {
                    "target": {
                      "class": "#32768"
                    },
                    "event": "mouse",
                    "param": [
                      [
                        20,
                        10
                      ],
                      "left"
                    ],
                    "wait": 1
                  }
                ]
              },
              "postrun": [
                {
                  "action": "fileclean",
                  "params": [
                    "%USERPROFILE%\\Documents\\Navicat"
                  ]
                },
                {
                  "action": "regclean",
                  "params": [
                    "HKEY_CURRENT_USER\\Software\\PremiumSoft\\Navicat\\Servers"
                  ]
                },
                {
                  "action": "command",
                  "params": [
                    "echo",
                    "test"
                  ]
                }
              ]
            }
        ```
        
## ���г���
������ú󣬿ɹرյ�����־��Ȼ������Ƿ����ʵ���Զ��������ݿ�

### ��������
* ��cmd�����ñ�������ȡ��������־
    ```bash
       set APPLAUNCHER_DEBUG=0
    ```

### ���г���
* ��cmd��ִ�����³���
    ```bash
       AppLauncher.exe http://127.0.0.1:8080/req?app=navicat-premium
    ```
