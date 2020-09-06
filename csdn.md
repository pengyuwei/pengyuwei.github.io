# Excel无法vlookup事件

2017-07-24 18:20:00

```
最近由于工作关系，深入的用了一阵excel，并遭遇和处理了一系列关于excel数据的问题。
其中最有趣的一个，就是一个无法vlookup的问题。

问题记录如下：
excel中直接打开csv文件，看到类似如下的数据表（为清晰，使用16进制显示）：
00000000: 534e 2c44 4154 410d 0a41 092c 4461 7461  SN,DATA..A.,Data                
00000010: 310d 0a31 3233 3435 3738 3930 3132 092c  1..12345789012.,                                               
00000020: 4461 7461 340d 0a43 092c 4461 7461 330d  Data4..C.,Data3.                
00000030: 0a                                       .               


在另外一个数据表中，需要对SN号做关联操作。于是使用常用的vlookup进行关联，但是发现全部数据都只得到N/A：
SN	取值
A	#N/A
12345789012	#N/A
C	#N/A


在两个表里使用查询功能查询相应的sn，都可以查到。
于是使用sublime查看csv文件本身，发现这个csv中的sn号，后面统一附加了一个tab字符。
csv文件来自于一个软件系统，咨询研发，得到的答复是，sn里有一些号是纯数字，如果不加tab，会被excel显示为科学计数法，引发更多问题。
使用正则表达式移除掉全部tab之后，用excel直接打开，发现确实部分sn被显示为科学计数法，且无法恢复原始值。

经研究，发现excel对于此种情况，其实有处理方法，就是使用csv数据导入功能而不要直接打开csv，经实验，使用文本数据导入功能，并设定sn字段为文本，即可解决科学计数法问题，并且可以正确的vlookup。
由于太忙，研发团队拒绝对系统进行任何修改。同时，各种表格的数据来源非常复杂，大家基本都已经在基于这些excel数据在工作了。
因此，写了一段vba代码针对无法vlookup的excel文档的sn做了处理，解决了这些文档无法vlookup的问题：

Public Sub 去掉SN号两端的空格()
    ' TODO:首先把字段设置成文本格式
    Dim Rng1 As Range
    For Each Rng1 In Range("A2:A9999")
        ' 处理科学计数法问题
        On Error Resume Next
        If CStr(Val(Rng1.Value)) = Rng1.Value Then
            Rng1.Value = "'" & Rng1.Value
        End If
        Rng1.Value = Trim(Rng1.Value)
        Rng1.Value = Replace(Rng1.Value, vbTab, "")
        DoEvents
    Next
End Sub
使用的时候，需要修改range的范围，和sn的实际范围对应。

没有使用UsedRange.Rows.count之类的方法，是因为期间发现了很多人的很多表格，数据可能并不多，但rows.count都是一个巨大的数字。（一般这些数据也都是来自于某软件系统导出的数据，看来非常不靠谱），解决这个问题是另外一个话题了，暂且不表。

有一个花絮是，曾经在一个同事的表格，发现了部分匹配成XX的值，实际是因为sn匹配失败，导致得到了其他结果。我深深的怀疑，在此前的工作中，有多少数据是刚好经过了这个坑被计算出来的，这又引发了哪些连锁的数据错误，而这些数据如果刚好被用于计算公司的成本收入或者其他重要的用途，导致的判断错误最终会引发多大的后果。
```

# 如何提交代码给openstack

2013-07-30 11:26:31

```
如果想为openstack做贡献，最好的方法就是帮助社区完成blueprint或者做bugfix。代码的提交需要遵循社区的一些基本要求，以下内容是去年对openstack社区的参与过程中的一些总结。
原文地址：http://blog.csdn.net/ffb/article/details/9625011

流程
    注册一个openid    
申请个人CLA证书    
申请公司CLA证书(个人不需要做本步骤)    更新贡献者列表，公司栏写上所属公司的名字    加入OpenStack Contributors组(必须)和OpenStack组 https://launchpad.net/~openstack-cla/+join(必须)    设置SSH Keys（复制本地~/.ssh/id_rsa.pub的内容即可）    认领一个blueprint/bug(这步可以跳过)    git clone代码到本地，配置user.name和user.email和openid中登记的一致    在期限内修改，并通过所有测试(不通过测试一定会被拒)。代码的一个基本的要求是要符合 PEP8 规范。        |__如果超过期限，去界面上点击“Restored”按钮即可    用git review命令提交审核    等待评审结果    按照评审要求修改代码，用git commit …. -amend提交修改    再次git review直到成功测试要求
import库的名称需要按照字母顺序排列

pep8检测：
sudo apt-get install pep8
~/nova$ pep8 .

nosetest:
sudo pip install nose
~/nova$ nosetests .

novatest:
~/nova$ sudo ./run_tests.sh [api/xxx/xxxx.py]
例如：./run_tests.sh test_db_api

tempest-devstack：
cd devstack; source exerciserc; ./exercise.sh注释要求

格式分为三部分，最前面一行是本地修改的简述，后面空一行之后写本次修改的详细描述，后面再空一行写本次修改对应的bugid或者bpid，然后紧接着写changeid。 系统会根据注释中的Change-Id去判断这个提交是属于那个bp的，fixbug和implement blueprint要写在changeid前面一行。Implement bp:efficient-limiting.

1.add limit param to db.instance_get_all_by_filters()
2.execute limit before sqlarchmy get_all()

Fixes: bug #1003373
Implements: blueprint xxxxxxxxxxx
Change-Id: Iea3eeb7b51194b6017d624506aafc6469d7338e4
参考文档：Summary_of_GIT_commit_message_structure |Information_in_commit_messages
更新要求

在执行git review之前，应该确保review是最新的，使用如下命令更新当前代码到最新版本：git fetch origin master
git rebase FETCH_HEAD
git add .
git commit --amend
git review如果rebase的时候发生冲突，应该手工解决冲突之后执行git rebase --continue

F.A.Q.

[Q]由于服务器的原因导致提交review后的代码测试失败。
[A]
对这个patch执行review，如果是SmokeStack，输入reverify，如果是Jenkins，输入recheck即可让其重新进行测试

[Q]如何在家继续修改
[A]
在公司提交patch去review后，在家继续进行修改，可以
1. 本地执行
     git-review -d review_number
    如，git-review -d 12859
    这个步骤会校验ssh-key

或者
2. 将Jekins上的改动merge到本地。
    在review按钮附近有按钮



参考文档

社区：nova bugs |

review.openstack.org | 
blueprint |
文档：GerritWorkflow |

assign-commit-and-review | 
progit
```

# ValueError: ('No requirements found', '# Horizon Core Requirements')的调试解决方法

2013-06-26 16:53:22

```
我在一台不能访问外网的CentOS6上从源码安装Openstack-horizon grizzly版本的时候，碰到了如下的错误：
[root@xxx horizon]# python setup.py install
running install
Traceback (most recent call last):
  File "setup.py", line 28, in <module>
    d2to1=True)
  File "/usr/local/lib/python2.7/distutils/core.py", line 152, in setup
    dist.run_commands()
  File "/usr/local/lib/python2.7/distutils/dist.py", line 953, in run_commands
    self.run_command(cmd)
  File "/usr/local/lib/python2.7/distutils/dist.py", line 972, in run_command
    cmd_obj.run()
  File "/usr/local/lib/python2.7/site-packages/pbr/packaging.py", line 318, in run
    _pip_install(links, self.distribution.install_requires, self.root)
  File "/usr/local/lib/python2.7/site-packages/pbr/packaging.py", line 100, in _pip_install
    " ".join(_wrap_in_quotes(_missing_requires(requires)))),
  File "/usr/local/lib/python2.7/site-packages/pbr/packaging.py", line 88, in _missing_requires
    pkg_resources.Requirement.parse(r)) )]
  File "build/bdist.linux-x86_64/egg/pkg_resources.py", line 2870, in parse
ValueError: ('No requirements found', '# Horizon Core Requirements')其中，setup.py中提到的依赖项是pbr和d2to1两个模块，于是尝试执行

# python -c "import pbr"
# python -c "import d2to1"
# 

但是发现pbr和d2to1两个模块都存在，不明白到底缺少了啥，horizon的提示信息里没有这个信息。于是按照提示编辑出错的代码：

vi /usr/local/lib/python2.7/site-packages/pbr/packaging.py +84
做了如下修改把正在检测的模块名称打印出来，这样就知道究竟是哪个模块不存在了：
73 def showdebug(r):
 74     print "--> Checking requires:" + r
 75     return True
 76     
 77 def _missing_requires(requires):
 78     """Return the list of requirements that are not already installed.
 79 
 80     Do this check explicitly, because it's very easy to see if a package
 81     is in the current working set, to avoid shelling out to pip and attempting
 82     an install. pip will do the right thing, but we don't need to do the
 83     excess work on everyone's machines all the time (especially since tox
 84     likes re-installing things a lot)
 85     """
 86     return [r for r in requires
 87             if showdebug(r) and (not pkg_resources.working_set.find(
 88                 pkg_resources.Requirement.parse(r)) )]经过实验，发现所有的依赖组件都是写在requirements.txt这个文件里的，抛出异常的代码没有处理井号注释的情况。所以提示信息里的
# Horizon Core Requirements
实际指的是requirements.txt文件里这条注释下面的那一行依赖项。按照提示的名称从https://pypi.python.org/pypi/Django/1.5.1中下载相应的源代码安装即可。

最后列举一下实际的依赖项(个别不能使用最新版本的做了版本标注)：
django_compressor-1.3django-appconfsixdjango_openstack_auth-1.0.11python-keystoneclientiso8601prettytablerequestssimplejsonoslo.confignetaddrpython-cinderclientwarlockjsonpatchjsonpointerpyOpenSSLjsonschema<2python-heatclientpython-glanceclienthttplib2python-novaclientpython-quantumclientcliffpyparsing>=1.5.6,<2.0pytzlockfile
其中执行pyparsing这个模块的源代码有语法错误：

[pyparsing-2.0.0]# python setup.py install
Traceback (most recent call last):
  File "setup.py", line 9, in <module>
    from pyparsing import __version__ as pyparsing_version
  File "/root/pyparsing-2.0.0/pyparsing.py", line 629
    nonlocal limit,foundArity
                 ^
SyntaxError: invalid syntax
nolocal是python3的新特性，用于修改作用域之外的非全局变量。所以在openstack环境中应该使用更低版本的pyparsing包，经查询安装包，要求的版本号为>=1.5.6到<2.0之间。（已经标注在上面的列表中)
```

# 一个有关PHP随机数的坑...

2013-06-06 15:41:41

```
php中获取随机数的方法很简单，使用rand函数就可以了

int rand ( int $min , int $max )
一句调用就可以获得指定范围的随机数。但是大家都知道，计算机中使用的随机数实际是伪随机数，一般来说，为了增加随机性，我们还会习惯在调用之前设置一下随机种子：


void srand ([ int $seed ] )
按照其他语言的习俗，会在srand的参数里传递一个时间值，一般会传递当前时间的毫秒值或者微秒值进去。虽然从PHP4.2开始，调用rand的时候会自动调用srand，所以srand调用是一个并非必须的操作。


PHP中可以使用microtime()函数来获取随机数。于是，在一个一般性随机数需求场景下，我们就可以使用下述代码获取随机数了

<?php
    srand(microtime());
    echo rand(1, 25).PHP_EOL;
    echo rand(1, 25).PHP_EOL;
?>
执行代码，我们得到了两个随机数。看似不错，但是再次执行，却发现得到的随机数和上次的一模一样。
这是啥状况？我们明明已经设置srand种子为当前时间的毫秒值了。
查阅文档，才发现其中的问题，原来在不带参数的情况下，mircotime函数会以"msec sec" 的格式返回一个空格分隔的字符串，经过自动类型转换，srand实际得到的参数值是0，在固定随机种子的情况下，会得到固定的随机序列，因此每次执行脚本都会得到相同的随机数。
从PHP5开始，microtime增加了一个$get_as_float参数，通过传递true，可以让microtime返回一个当前毫秒的float值，由于返回值小数点之前是当前的秒值，因此对结果再乘以1000把小数点扩展到毫秒级别，这样就可以安全的获取随机数了：

<?php
    srand(microtime(true) * 1000);
    echo rand(1, 25).PHP_EOL;
    echo rand(1, 25).PHP_EOL;
?>

连续访问两次，得到了不同的随机数，再写一个bash脚本：

for i in $(seq 1 1 100)
do
    curl http://127.0.0.1/rnd.php
    echo 
done连续跑100次，测试通过。



其实。。。
前例中的代码会报告一个

PHP Notice: A non well formed numeric value encountered

警告。但是如果脚本是跑在服务或者后台进程中，则可能不容易发现问题。

或者。。。
PHP中已经有了一个mt_rand()的函数用来替换古老的rand，可以自动播种并且效率比rand高四倍。。。好吧，看来研究旧有问题和学习新鲜知识一个都不能少。。。
```

# Diffusion User Guide: Symbol Indexes (Article)

2013-05-17 15:04:10

```
http://www.phabricator.com/docs/phabricator/article/Diffusion_User_Guide_Symbol_Indexes.html
Phabricator » Diffusion User Guide: Symbol Indexes (Article)
Article Diffusion User Guide: Symbol Indexes
Defined    src/docs/userguide/diffusion_symbols.diviner:1
Group    Application User Guides
Table of Contents
    Overview
    Populating the Index
    Configuring Differential Integration
Guide to configuring and using the symbol index.
OverviewPhabricator can maintain a symbol index, which keeps track of where classes and functions are defined in the codebase. Once you set up indexing, you can use the index to do things like:
Phabricator 可以维持一个符号索引, 他可以保持对代码库中类和函数的跟踪. 当生成索引之后，你可以做类似下面的事情:

    link symbol uses in Differential code reviews to their definitions
    allow you to search for symbols
    let the IRC bot answer questions like "Where is SomeClass?"
    在Differential code reviews中根据定义链接到符号
    允许你查询符号    让IRC机器人可以回答类似"Where is SomeClass?"的问题

NOTE: Symbol indexing is somewhat new, and has broader support for PHP than for other languages.
注意: 符号索引比较新, 在PHP中的支持比其他语言更广泛.

Populating the Index
填充索引

To populate the index, you need to write a script which identifies symbols in your codebase and set up a cronjob which pipes its output to:
./scripts/symbols/import_project_symbols.php
Phabricator includes a script which can identify symbols in PHP projects:
./scripts/symbols/generate_php_symbols.php
Phabricator also includes a script which can identify symbols in any programming language that has classes and/or functions, and is supported by Exuberant Ctags (http://ctags.sourceforge.net):
./scripts/symbols/generate_ctags_symbols.php
If you want to identify symbols from another language, you need to write a script which can export them (for example, maybe by parsing a ctags file).
The output format of the script should be one symbol per line:
<context> <name> <type> <lang> <line> <path>
For example:
ExampleClass exampleMethod function php 13 /src/classes/ExampleClass.php
Context is, broadly speaking, the scope or namespace where the symbol is defined. For object-oriented languages, this is probably a class name. The symbols with that context are class constants, methods, properties, nested classes, etc. When printing symbols
 without a context (those that are defined globally, for instance), the <context> field should be empty (that is, the line should start with a space).
Your script should enumerate all the symbols in your project, and provide paths from the project root (where ".arcconfig" is) beginning with a "/".
You can look at generate_php_symbols.php for an example of how you might write such a script, and run this command to see its output:
$ cd phabricator/
$ find . -type f -name '*.php' | ./scripts/symbols/generate_php_symbols.php
To actually build the symbol index, pipe this data to the import_project_symbols.php script, providing the project name:
$ ./scripts/symbols/import_project_symbols.php yourproject < symbols_data
Then just set up a cronjob to run that however often you like.
You can test that the import worked by querying for symbols using the Conduit method differential.findsymbols. Some features (like that method, and the IRC bot integration) will start working immediately. Others will require more configuration.
Configuring Differential Integration
To configure Differential integration, you need to tell Phabricator which projects have symbol indexes you want to use, and which other projects they should pull symbols from. To do this, go to Repositories -> Arcanist Projects -> Edit as an administrator.
 You need to fill out these fields:
    Repository: Associate the project with a tracked repository.
    Indexed Languages: Fill in all the languages you've built indexes for.
    Uses Symbols From: If this project depends on other projects, add the other projects which symbols should be looked for here. For example, Phabricator lists "Arcanist" and "libphutil" because it uses classes and functions from these projects.
Once you've configured a project, new revisions in that project will automatically link symbols in Differential.
NOTE: Because this feature depends on the syntax highlighter, it will work better for some languages than others. It currently works fairly well for PHP, but your mileage may vary for other languages.
```

# 改变MySQL的默认编码

2013-05-07 17:29:00

```
/etc/mysql/my.cnf
[mysqld]
character_set_server = utf8
collation-server = utf8_unicode_ci
init_connect='SET collation_connection = utf8_unicode_ci'
init_connect='SET NAMES utf8'
skip-character-set-client-handshake
[client]
default-character-set = utf8 
重启服务，查看：
show variables like '%character%';
得到
New client character set: latin1
Connected.character_set_client: utf8
character_set_connection: utf8
character_set_database: utf8
character_set_filesystem: binary
character_set_results: utf8
character_set_server: utf8
character_set_system: utf8
character_sets_dir: /usr/share/mysql/charsets/ 还有一种方法，重新编译libmysqlclient， 加-DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci  参数。但我没有实验是否有效。
cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DWITH_EXTRA_CHARSETS=complex \
    -DDEFAULT_CHARSET=utf8 \
    -DDEFAULT_COLLATION=utf8_general_ci \
    -DWITH_READLINE=1 \
    -DENABLED_LOCAL_INFILE=1 \
    -DENABLED_PROFILING=1 \
```

# php中的mysql连接字符串注意事项

2013-05-07 16:32:43

```
原帖地址：http://blog.csdn.net/ffb/article/details/8895630

php里有三套操作mysql的库，分别是自带的mysql系列函数、mysqli和mysqlpdo。这三套库的下层又使用了两个数据操作引擎，分别是libmysql和mysqlnd，具体使用哪个引擎由php编译时决定。
在实际使用这三个库的时候，存在一个小的问题，就是连接字符串的写法。对于host:port的格式，在libmysql中和mysqlnd中支持情况有差异。所以如果你使用了这种写法又切换了引擎或者使用的库，则可能导致问题。

下面结合新浪云计算SAE中的数据库操作列举一下各种情况，如非说明，默认均是libmysql环境下，具体是：php内置mysql函数的正确写法：
mysql_connect('127.0.0.1:3306', $user, $password);
其中第一个参数是host:port格式，libmysql引擎、mysqlnd和SAE均支持这种格式的写法。
官方的说明在：http://cn2.php.net/manual/en/function.mysql-connect.php

mysqli中的正确写法：
$conn = new mysqli("127.0.0.1", $user, $pwd, $db, "3306");
如果写成：
$conn = mysqli_connect('127.0.0.1:3306', $user, $password);
或：
$conn = new mysqli("127.0.0.1:3306", $user, $pwd);
其中第一个参数是host:port格式，原生mysqli不支持这种写法，在SAE中支持此写法。
官方的说明在：http://cn2.php.net/manual/en/function.mysqli-connect.php

pdomysql中的正确写法：
$conn= new PDO('mysql:host=127.0.0.1;port=3306', $user, $password);
原生mysqlpdo和SAE均支持此写法。
如果写成：
$conn= new PDO('mysql:host=127.0.0.1:3306', $user, $password);
原生mysqlpdo和SAE均不支持此种写法。但是在mysqlnd引擎环境下，支持此写法。
官方的说明在：http://cn2.php.net/manual/en/pdo.construct.php

综上得到针对host:port格式的支持情况的列表：
libmysql引擎下：
mysql：支持
mysqli：不支持（SAE中做了支持）
mysqlpdo：不支持

mysqlnd引擎下：
mysql：支持
mysqli：支持
mysqlpdo：支持

结论：php中操作mysql数据库的时候，从兼容性角度考虑，最好明确指示port参数，而不要使用冒号分隔的缩写写法。
```

# “MySQL server has gone away”的重现方法(PHP)

2013-04-12 10:41:38

```
如果想调试“MySQL server has gone away”的问题，可以这样重现：
修改配置文件：

sudo vi /etc/mysql/my.cnf
做如下修改：


[mysqld]
wait_timeout = 30
interactive_timeout = 30
重启服务：


sudo /etc/init.d/mysql restart
编写如下php脚本


<?php
$link = mysql_connect('127.0.0.1', 'root', 'root');
if (!$link) {
    die('Could not connect: ' . mysql_error());
}
echo 'Connected successfully';

sleep(31);
$result = mysql_query('show variables;');
if (!$result) {
    die('Invalid query: ' . mysql_error());
}
while ($row = mysql_fetch_assoc($result)) {
    var_dump($row);
}
mysql_free_result($result);

mysql_close($link);
?>

执行：
$ php mysql.php 
Connected successfully
Invalid query: MySQL server has gone away
或者在命令行下等30秒也可以看到这个错误了：
mysql> select variables like '%timeout';
ERROR 2006 (HY000): MySQL server has gone away
No connection. Trying to reconnect...
Connection id:    40
Current database: *** NONE ***然后你就可以想干啥干啥了，比如加个mysql_ping让他实现自动重连：

<?php
function get_conn() {
    $conn = mysql_connect('127.0.0.1', 'root', 'root');
    if (!$conn) {
        die('Could not connect: ' . mysql_error() . '\n');
    }
    return $conn;
}

$conn = get_conn();

sleep(31);
if (!mysql_ping($conn)) {
    mysql_close($conn);
    $conn = get_conn();
    echo 'Reconnect\n';
}

$result = mysql_query('show variables;');
if (!$result) {
    die('Invalid query: ' . mysql_error());
}
while ($row = mysql_fetch_assoc($result)) {
    var_dump($row);
}
mysql_free_result($result);

mysql_close($conn);
?>

另外，php文档里说mysql_ping可以自动重连，但经实验实际上还是需要用户自行处理重连的问题（也可能我的参数设置不对）。
如果使用的是C/C++，可以在连接建立后使用如下方法让mysql_ping具有自动重连功能：
char mysql_reconnect = 1; 
mysql_options(mysql->conn, MYSQL_OPT_RECONNECT, (char *)&mysql_reconnect);
```

# php的咨询文件锁定：flock

2013-04-03 16:20:12

```
最近在研究php，碰到了一个问题，我使用如下代码锁定一个文件句柄

<?php
$filename = "/tmp/lock.txt";

$fp = fopen($filename, "r+");
if (!$fp) {
    die("open failed.");
}

if (flock($fp, LOCK_EX)) {  // 进行排它型锁定
    sleep(20);
    $count = (int)fgets($fp);
    $count += 1;
    fseek($fp, 0);
    fwrite($fp, (string)$count);
    fflush($fp);            // flush output before releasing the lock
    flock($fp, LOCK_UN);    // 释放锁定
} else {
    echo "Couldn't get the lock!";
}

fclose($fp);
?>
访问，然后在sleep的20秒内尝试使用vi编辑/tmp/lock.txt，发现可以成功修改文件内容而不需要等待第一个脚本结束。经琢磨文档，发现这里有个概念叫"咨询文件锁定"，就是说所有访问程序必须使用同一方式锁定才会生效, 否则它不会工作。

尝试使用如下代码在20秒内访问：

<?php
$filename = "/tmp/lock.txt";

$fp = fopen($filename, "r+");
if (!$fp) {
    die("open failed.");
}

if (flock($fp, LOCK_EX)) {  // 进行排它型锁定
    $count = (int)fgets($fp);
    echo $count;
    $count += 1;
    flock($fp, LOCK_UN);    // 释放锁定
} else {
    echo "Couldn't get the lock!";
}

fclose($fp);
?>

发现阻塞成功（第二个脚本需要等待第一个脚本结束才能继续运行）。

那么，什么叫同一种方式锁定呢？继续做如下实验：
A组：

尝试脚本1的flock参数修改为LOCK_SH，脚本2不变，试验，发现阻塞成功；（因为2要独占，要等共享锁结束）尝试脚本1和脚本2的flock参数都修改为LOCK_SH，发现脚本2会可以返回结果而不用等待脚本1执行结束；（都是共享，无所谓了）
B组：

尝试将脚本2的flock参数修改为LOCK_SH，脚本1不变。阻塞成功。（因为被1独占了）

对照组：

尝试将脚本2的fopen参数修改为"r"，运行A组实验，现象一样；（和打开文件的参数无关）尝试将脚本1和2的fopen参数都修改为"w+"，运行A组实验，现象一样；尝试将脚本1和2的fopen参数都修改为"w+"，运行B组实验，现象一样；
所以，锁定和LOCK_*参数相关。和打开文件的方式无关。而vi可以编辑的问题，是因为这个锁是线程级别的。
```

# 贝尔金无线路由器由OpenWRT刷DD-WRT

2011-12-24 13:00:10

```
贝尔金的Belkin  F5D7231-4  N10117无线路由器
配置是：4MFlash/64M内存，带USB口
型号：Belkin F5D7230-4 v1444
之前刷的是OpenWRT(openwrt-brcm-2.4-squashfs.trx)，最近在研究中继的时候被我不小心配错了，结果再也不能用了，用之前的IP无法登录进入，但是能看到无线信号且可以连接，但是无法使用。
于是决定刷DDWRT，DD官网下载了

dd-wrt.v24_micro_generic.bin

用官网的tftp工具设置好，然后打开cmd窗口，ping 192.168.2.1 -t

按住路由器reset键10秒钟，松手，然后立刻在tftp工具里回车，上传成功。



Request timed out.
Reply from 192.168.2.1: bytes=32 time=1ms TTL=100
Reply from 192.168.2.1: bytes=32 time=1ms TTL=100
Reply from 192.168.2.1: bytes=32 time=1ms TTL=100
Reply from 192.168.2.1: bytes=32 time=1ms TTL=100
Request timed out.



重启后用浏览器访问192.168.1.1即可
```

# telnet协议解析中的难点

2011-10-17 16:13:54

```
类似下面的数据：
telnet终端的vi模式下，用户输入了一个echo aa bb cc dd命令，然后回车执行

请求：
0000   0d 00                                            ..
响应：
0000   0d 0a                                            ..
响应：(echo的执行结果和提示符)
0000   61 61 20 62 62 20 63 63 20 64 64 0d 0a 1b 5d 30  aa bb cc dd...]0
0010   3b 70 79 77 40 77 6f 72 6b 2d 35 31 3a 20 7e 07  ;pyw@work-51: ~.
0020   70 79 77 40 77 6f 72 6b 2d 35 31 3a 7e 24 20     pyw@work-51:~$ 
请求：
0000   1b                                               .
请求：(调取上一个命令)
0000   6b                                               k
响应：(得到上一个命令，光标右移的15个字节实际为提示符的长度)
0000   65 63 68 6f 20 61 61 20 62 62 20 63 63 20 64 64  echo aa bb cc dd
0010   20 0d 00 1b 5b 43 1b 5b 43 1b 5b 43 1b 5b 43 1b   ...[C.[C.[C.[C.
0020   5b 43 1b 5b 43 1b 5b 43 1b 5b 43 1b 5b 43 1b 5b  [C.[C.[C.[C.[C.[
0030   43 1b 5b 43 1b 5b 43 1b 5b 43 1b 5b 43 1b 5b 43                                                  C.[C.[C.[C.[C.[C
请求：(光标跳转到下一个单词处)
0000   77                                               w
响应：(右移5个字节为echo命令和后面的空格)
0000   1b 5b 43 1b 5b 43 1b 5b 43 1b 5b 43 1b 5b 43     .[C.[C.[C.[C.[C
请求：(cw命令为剪切(删除)当前光标所在单词)
0000   63                                               c
0000   77                                               w
响应：(删除当前光标处的单词)
0000   1b 5b 32 50                                      .[2P

难点在于，从协议本身，我们是无法得知哪一部分数据是提示符的，这就会造成后续的光标移动和实际情况不符。
而提示符信息又是一个随意配置的，这个信息只有服务器掌握，从客户端和中间人都无法直接得知。
在ubuntu系统上，配置提示符非常的容易：
export PS1=提示符串即可
提示符可以是任意字符串且支持转义，甚至可以内容为空。对于中间人来说，自动处理只能通过一些特征数据(如\r\0)来做一些兼容性处理。目前一直没有找到特别好的解决方法。
```

# 一个很深的bug - 句柄被异常关闭

2011-05-13 11:55:00

```
昨天系统出现了问题，现象是日志从进入守护进程模式后就再也不出了，检查了半天也没查出问题。
下午的代码走查会议，无意中找到了问题的原因。
原来一个模块新加的初始化函数被放到了日志模块的初始化函数之前，那个初始化函数对一个未初始化的句柄数组逐一执行了close操作。
数组中其中一个成员为0-3之间的数值，导致了日志模块初始化的时候，open日志文件时候得到的句柄为0-3之间的数字，然后进入守护进程的函数里在fork之后执行了对0-3的close，这导致了日志文件的句柄被关闭，从而使得后面就再也没有日志了。
 
改那个新模块的close操作为直接把句柄设置为-1，问题解决。
```

# zlib解压缩时对破损数据的处理

2011-03-31 11:19:00

```
zlib解压缩的时候碰到数据截断怎么办？
最近碰到了一个问题，被zlib压缩的数据的前段数据丢失，导致后续数据无法解压缩，但经过实验，发现zlib已经提供的很强的容错能力，问题最终解决。
 
实验过程举例如下：
 
方式1：使用Z_SYNC_FLUSH参数分段压缩，整体解压缩
 
while ((i = read(r_fd, in_buf, 3)) > 0) {
in_len += i;
buffer_compress(in_buf, i, ptr, &out_len);
ptr += out_len;
}
buffer_uncompress(compress_buf, compress_buf_len, uncompress_buf, &un_len); 
解压缩成功。
 
方式2：使用Z_PARTIAL_FLUSH参数分段压缩，整体解压缩
（代码同方式1）
解压缩成功
 
方式3：使用Z_PARTIAL_FLUSH参数分段压缩，同时解压缩
 
while ((i = read(r_fd, in_buf, 3)) > 0) {
in_len += i;
buffer_compress(in_buf, i, ptr, &out_len);
buffer_uncompress(ptr, out_len, uncompress_buf, &un_len);
printf("1.%s[%d, %s] /n", uncompress_buf, un_len, __FILE__);
} 
解压缩成功
 
 
方式4：使用Z_SYNC_FLUSH参数分段压缩，同时解压缩
 
（代码同上）
解压缩成功
 
 
 
方式5：使用Z_SYNC_FLUSH参数分段压缩，之后从中间解压缩
 
 
while ((i = read(r_fd, in_buf, 3)) > 0) {
in_len += i;
buffer_compress(in_buf, i, ptr, &out_len);
ptr += out_len;
}
compress_buf_len = ptr - compress_buf;
end = ptr;
printf("in len=%d, compressed len=%d /n", in_len, compress_buf_len);
ptr = compress_buf + 5;
buffer_uncompress(ptr, compress_buf_len - 5, uncompress_buf, &un_len);
printf("1.%s[%d, %s] /n", uncompress_buf, un_len, __FILE__); 
 
 
 
解压缩失败，错误信息：
buffer_uncompress: inflate returned -3
解压缩方法改为：
 
 status = inflateSync(&incoming_stream);
 status = inflate(&incoming_stream, Z_SYNC_FLUSH); 
解压缩成功，得到了从截断处开始的数据
 
 
 
方式6：同方式4，但解压缩前执行inflateSync
 
解压缩出错，错误信息：Illegal seek
 
由此可见，inflateSync可以处理数据截断的问题，但是只有确定数据是截断的才能调用。
另外在截断的数据的前面附加0x78,0x9c或者0x0,0x0,0xFF,0xFF也可以实现正常解压缩。
0x78,0x9c是zlib数据头(非固定，参考RFC 1951)，而00 00 FF FF是zlib容错方式的数据块头。
又经多次实验，发现zlib压缩的特点，是可以逐块压缩，逐块解压缩；或者整体压缩，然后逐块解压缩；
但是不能逐块压缩，然后跨块解压缩。（不inflateSync的话）
 
 
 
附解压缩函数源代码：
 
void
buffer_uncompress(char* input_buffer, int in_len, char* output_buffer, int *out_len)
{
u_char buf[4096];
int status;
incoming_stream.next_in = input_buffer;
incoming_stream.avail_in = in_len;
/* Set up fixed-size output buffer. */
incoming_stream.next_out = buf;
incoming_stream.avail_out = sizeof(buf);
status = inflateSync(&incoming_stream);
status = inflate(&incoming_stream, Z_SYNC_FLUSH); // Z_SYNC_FLUSH/Z_PARTIAL_FLUSH
switch (status) {
case Z_OK:
memcpy(output_buffer, buf,sizeof(buf) - incoming_stream.avail_out);
*out_len = sizeof(buf) - incoming_stream.avail_out;
return;
case Z_BUF_ERROR:
perror("zlib : ");
/*
* Comments in zlib.h say that we should keep calling
* inflate() until we get an error.  This appears to
* be the error that we get.
*/
return;
default:
inflate_failed = 1;
printf("buffer_uncompress: inflate returned %d/n", status);
}
} 
编译方法：
gcc -lz compress.c stream_test.c -g
 
 
```

# 日志文件被追杀之谜

2011-03-25 15:12:00

```
现象描述：
执行脚本down.sh，内容:
mkdir -p bak2log
killall -9 dt
sleep 1
echo '-----------------------------------------------------'
tftp -g -r dt 192.168.42.219
mv ./log.d/* ./bak2log/
...（其他内容）
其中的dt会常打开日志文件log.d/dt.log
脚本的功能为杀掉dt，备份日志（mv到其他目录），下载新的dt程序，重启启动dt（略）
 
执行后发现log.d下只生成了一个0字节的新文件，但是没有文件内容，查看打开句柄情况：
 
# ls -l /proc/8977/fd/
lr-x------    1 0        0              64 Mar 25 15:02 0 -> /dev/null
lrwx------    1 0        0              64 Mar 25 15:02 1 -> /dev/null
lrwx------    1 0        0              64 Mar 25 15:02 10 -> /dev/audit_kdi2010v1
l-wx------    1 0        0              64 Mar 25 15:02 11 -> /dev/null
lrwx------    1 0        0              64 Mar 25 15:02 2 -> /dev/null
lrwx------    1 0        0              64 Mar 25 15:02 3 -> /memory_module
lrwx------    1 0        0              64 Mar 25 15:02 4 -> /sysinfo_module
lrwx------    1 0        0              64 Mar 25 15:02 5 -> socket:[533]
lrwx------    1 0        0              64 Mar 25 15:02 6 -> socket:[538]
l-wx------    1 0        0              64 Mar 25 15:02 7 -> /v_dt/bak2log/dt.log
l-wx------    1 0        0              64 Mar 25 15:02 8 -> /v_dt/.dt.lock
 
发现绑定的竟然是备份目录下的日志文件
尝试延长sleep的值，无效
尝试改mv为cp+rm，问题解决。
但是百思不得其解，为什么mv后的文件会依然被之后启动的进程所使用。
```

# 常用的编译环境

2011-03-12 14:20:00

```
tilda-0.09.6 in ubuntu 10.04
sudo apt-get source tilda
sudo apt-get install flex libglade2-dev libvte-dev libconfuse-dev
vi key_grabber.c 注释掉行194（gdk_x11_window_set_user_time）
vi tilda_window.c 注释掉行255 （tilda_window_setup_keyboard_accelerators）里面的快捷键绑定
 
sudo cp ../tilda.png /usr/local/share/pixmaps/
默认配置文件：
sudo cp ../tilda.glade /usr/local/share/
 
重新make运行即可
 
```

# 一个很好很先进的东西，往往被一个粗糙的用户接口毁掉

2011-01-29 22:10:00

```
父母新换了一个名牌的高档的微波炉，还不会用，让我研究一下，我这个搞IT的研究了半天，发现竟然真的搞不清怎么用。于是只能去看说明书，洋洋洒洒几十页，粗略看了一遍，又几经实验，终于。。。会热剩菜了。。。由于是数字控制，这个微波炉每次接通电源后要经历一次初始化过程，我计算了一下，首次插电初始化时间超过一分钟，之后初始化大约需要半分钟，我甚至怀疑这里面是不是装了一个Vista系统，一个微波炉，启动比我512MB内存跑XP还慢。操作菜单是中文英文数字甚至代号混合的，比如P-100代表微波强度为强，而且要按一定的顺序按按钮才能进入微波热剩菜模式，所以不看说明书是不可能会用的。（在我看来，热剩菜是微波炉唯一的用途）
回想过去的老微波炉，我要做的所有事情就是打开炉门，放进剩菜，关上门，拧两分钟即可，多么的简洁。
```

# 编码问题：svn无法更新

2011-01-26 11:23:00

```
 
最近的Ubuntu10.04桌面执行了自动更新之后，终端窗口的编码好像有点问题。
 
其中一个问题是，我用ssh连接到开发机(Fedora5+GB2312编码)，执行svnup出错：
svn: Can't convert string from 'UTF-8' to native encoding:
svn: datacenter/hook/?/229?/143?/130?/232?/128?/131?/232?/181?/132?/230?/150?/153
 
过去是正常的，不知道为什么出错。
解决办法是：删除源代码，端口窗口的编码选择GBK，然后重新svn co就行了。
 
如果汉字显示为乱码，可以执行
LANG=en_US
即可显示为英文
 
但是再次执行svn up又不行了，最终，发现是文件名使用了中文造成，设置了编码后，文件系统中的文件名用的编码可能和环境不同就会造成类似问题。
 
'参考资料'四个汉字的GBK编码为：
B2 CE BF BC D7 CA C1 CF
 
UTF-8编码为：
E5 8F 82 E8 80 83 E8 B5  84 E6 96 99
 
再看svn的错误信息：
svn: datacenter/hook/?/229?/143?/130?/232?/128?/131?/232?/181?/132?/230?/150?/153
翻译成16进制是
E5 8F 82 E8 80 83 E8 B5  84 E6 96 99
说明这个文件夹在提交的时候使用的UTF-8编码，而系统环境设置的是GB2312，因此造成SVN对这个文件夹的处理出错。
 
因此，如果在Linux服务器上做开发等工作，建议最好还是使用默认的也是被支持最好的UTF-8编码，可以减少很多不必要的麻烦。
如果实在要改成其他编码，也最好规定使用制度，人为保证文件内容编码，中文文件名编码务必统一。
 
```

# Windows两个界面设计缺陷在Linux的解决方法

2010-12-03 13:41:00

```
用Windows的时候我一直在抱怨的两个界面设计缺陷：模式窗体和抢焦点都在Linux下找到了解决方案。
 
模式窗体的问题，就是在Windows下，如果一个程序弹出了一个模式窗体（即弹出窗口关闭前，不能对父窗体进行操作），在Ubuntu下（GNOME）
是这样解决的：模式窗体的父窗体可以移动。
这看似是个简单的特性，却导致了易用性的大幅提升。对于我这样的偏执型使用者来说，我喜欢把窗体摆放在合适的位置以便最大化可视范围。当有窗体是模式窗体的时候，父窗体是无法移动的（父窗体一般都会占很大面积），此时如果我想看下被父窗体挡住的其他窗体的内容，就会非常的不便。GNOME下模式窗体的父窗体可以移动这个小小的设计，完美的解决了这个问题。
 
 
抢焦点的问题，当输入东西的时候，忽然弹出一个窗口，结果我输入的东西就跑那个窗口去了，如果那个窗口不接受输入，就白输了。
比
如，当你在QQ聊天的时候，输入了一句中文，输到一半的时候，QQ新闻弹出来了，它弹出来之后自动变为当前窗口，这个时候一般你的输入速度会比较快，并且
可能在低头看键盘，所以后一半被输入到了QQ新闻的界面里，但它是不接受输入的，所以后半句丢失了！！你还得用鼠标或者键盘再切换回原来的窗口继续输入！
（可能在继续输入的时候，MSN每日焦点又弹出来了，烦不胜烦）
或者在输入哪个论坛的密码的时候，另外一个你之前打开的程序的主界面出来了（低配
置机器尤其容易碰到），由于后出现的程序自动获取了当前窗口和当前焦点，所以你的密码最后以明文的方式被输入到这个新窗口上了！！有一次就是这种情况，我
的QQ登录密码被输入到了新弹出的IE广告窗口的地址栏里，结果我的同学在旁边看到了，大声地念出我输入的QQ密码，气煞我也。
Windows的程序好像都倾向于启动后就立刻把用户的输入焦点抢过来。而根本不管用户当前正在干什么，这完全是对用户的不尊重，也是我认为的Windows最大的一个设计缺陷。
而kubuntu解决了这个我认为最大的一个易用性和人性化的问题。
解决方法：KDE主菜单--应用程序--设置--系统设置--窗口行为--焦点--避免抢占焦点的程度，设置为‘高’

然
后尝试几个启动速度较慢的程序，并在界面出现之前切换到一个输入窗口里，如gedit里输入文字，这个时候，你会发现，所有新弹出的窗口和软件界面，会自
动以非当前窗口的形式出现在你工作的窗体的后面，你的输入焦点再也不会被抢走了！！当然，你如果你需要在新的窗口里输入东西，只要切换到那个窗口就可以了。（或者把程度设置为‘中’，KDE会自动识别是否需要改变你的输入焦点）
也就是说，你想在哪里输入东西，完全是由你来决定的，程序再也不会‘强奸民意’了。
这两点都我好多年以来一直抱怨同时也梦寐以求的功能，现在终于在Linux下都找到了，很强的新鲜空气感。
```

# 利用VNC把远程图形界面显示在本地

2010-11-29 16:22:00

```
Ubuntu 10.04 IP=29.141
sudo vi gdm.schemas
修改以下内容：
1.
<key>security/DisallowTCP</key>
<signature>b</signature>
<default>false</default>
 
2.
<key>xdmcp/Enable</key>
<signature>b</signature>
<default>true</default>
3.
<key>xdmcp/DisplaysPerHost</key>
<signature>i</signature>
<default>2</default>    <--由1改为2
 
ffb@ffb-xen:/etc/gdm$ xhost +
access control disabled, clients can connect from any host
 
然后ssh登录远程计算机，执行：
export DISPLAY=192.168.29.141:0.0
[ffb@devserver detector]$ gedit
可以看到gedit的界面出现在本地了（并非直接VNC的全屏幕桌面都过来了）
```

# 国外原来是不能访问google music的

2010-06-19 18:09:00

```
一个在国外的朋友告诉我，在国外是不能访问google music，猜测可能是因为版权的问题，和墙无关
```

# 比金钱更重要的东西

2010-03-23 09:43:00

```
Google让我明白了，即使是商业社会里的商业公司，也可以为了自己的信念放弃金钱。
向Google致敬
```

# Ubuntu装机必备

2010-03-10 18:35:00

```
安装的时候虽然选择了简体中文，但是进入桌面后依然是英文菜单，这个时候之后从系统管理的语言中把语言都设置为汉语即可。
然后安装输入法，默认的ibus太难用，删除换scim
sudo apt-get remove ibus
sudo apt-get install scim-pinyin

安装QQ for Linux，

sudo gedit /usr/bin/qq
#!/bin/sh
export GDK_NATIVE_WINDOWS=true
cd /usr/share/tencent/qq/
./qq

这样QQ就不会频繁崩溃了(否则几句话就要崩溃一次)

 
如果使用wireshark抓包的话：
sudo chmod u+s /usr/bin/dumpcap
这样就可以用任何用户启动wireshark了(否则只有root能启动抓包)
 
安装FileZilla,传文件用，很好使，比WinSCP强多了（主要是能够支持不同编码）
sudo apt-get install filezilla
 
开发环境
sudo apt-get install build-essential
 
gedit的非常好用的编程插件：
symbol-browser/wordcompletion
symbol-browser装完后是没法用的，需要首先：
代码:

sudo apt-get install ctags
sudo apt-get install libgnomeprint2.2-0
sudo apt-get install libgnomeprintui2.2-0

然后在源代码目录执行ctags -R *
在gedit中启用插件，配置中选中"only load for active tab"，然后按F9，就可以看到源代码的函数／定义／常量等等信息，双击可以转到对应的源码
 
常用的16进制编辑器：
sudo apt-get install ghex
 
非常好用的文件对比工具，支持SVN和文件夹
sudo apt-get install meld
```

# linux下最难用的软件

2010-02-02 17:38:00

```
毫无疑问的QQ for Linux
在我的Ubunut9.10和Fedora12上，每天都在不停的崩溃，严重的时候一句话崩溃一次（对方能收到这句话）
 
本来以为WebQQ是个好的解决方案，但是WebQQ的验证码怎么输入都是错误的，难以理解
```

# webpy的缺陷

2010-02-02 14:59:00

```
如下代码
<table>
$len(lines)
$for itor in lines:
    <tr>
    $ (line, type) = itor
    $if type==1:
        <font size=2pt color=blue>
    $elif type==2:
        <font size=4pt color=red>
    $elif type==3:
        <font size=2pt color=red>
    $else:
        <font size=2pt color=black>
    $:line</font><br/>
    <tr>
</table>
 
得到：
 
        <table>
<tbody><tr>
    </tr><tr>
    </tr><tr>
    </tr><tr>
...35个（略）
    </tr><tr>
    </tr><tr>
            </tr><tr>
</tr></tbody></table>
 
怎么也理解不了Webpy的逻辑
后来终于搞明白了，原来是行结束的tr，我少了一个斜杠，webpy看来是严格按照html标签闭合情况进行处理的，兼容性不够好，当然，是在出错的情况下。
修改后，一切OK了
```

# redhat linux的自启动脚本

2010-01-15 15:41:00

```
/etc/rc.d/init.d下的脚本，需要a+x权限
#!/bin/sh
#
# ident "@(#)mipagent   1.1     99/11/06 SMI"
#
# Copyright (c) 1999 by Sun Microsystems, Inc.
# All rights reserved.
#

case "$1" in
'start')
        cd /www
        python index.py 80&
        ;;
'stop')
        pkill -x -u 0 -P 1 python index.py
        ;;
*)
        echo "Usage: $0 { start | stop }"
        exit 1
        ;;
esac
exit 0

然后在/etc/rc.d/rc3.d下建立连接即可
```

# 拖来拖去

2010-01-10 22:58:00

```
家里终于搭建好了比较理想的完整开发环境。
当我面对桌子上的三个屏幕的时候，十分想把一个窗口从一台显示器拖动到另外一个显示器上，
虽然Ubuntu910已经可以让我把窗口从一个虚拟桌面拖动到另外一个虚拟桌面，但是跨主机（甚至跨云）这种未来科技不知什么时候能出现。
上次在IBM大会，看到了让人震惊的IBM云计算，IBM的云已经可以管理（资源重分配）网络主机的磁盘／CPU，甚至内存等资源，而且精确到小数点，不得不让我目瞪口呆，原来印象中高高在上的云早已经落地。
```

# C#的DLL注册为COM，VB来调用

2009-08-21 11:12:00

```
非常实用的东西！过去知道这个方法的话可以解决多少问题啊
首先建立一个C#的DLL工程，写一个类
//Test.cs
namespace Test
{
public class MyTest
{
public string Fun()
{
return this.ToString();
}
}
}
，编译
然后在cmd里执行VS的vsvars32.bat设置环境变量，然后执行

regasmcscomtest.dll /tlb:cscomtest.tlb /codebase
Microsoft (R) .NET Framework 程序集注册实用工具1.1.4322.573
版权所有 (C) Microsoft Corporation1998-2002。保留所有权利。
RegAsm 警告:使用 /codebase注册未签名的程序集可能会导致程序集妨碍在同一台计算机
上可能安装的其他应用程序。/codebase开关旨在仅用于已签名的程序集。请为您的程序集
提供一个强名称并重新注册它。
成功注册了类型
程序集已被导出到“C:/Documents and Settings/pyw/My Documents/VisualStudio Proje
cts/cscomtest/bin/Debug/cscomtest.tlb”，类型库注册成功
 
然后打开VB或者VBS，写
set o =createobject("Test.MyTest")
msgbox o.Fun()
 
KO！成功了，这个效果相当于用VB调用C#，虽然是通过COM实现的，太酷了！
```

# googld文档忽然不能访问了

2009-03-11 10:26:00

```
从周一开始google文档忽然不能访问了，我的许多常用的信息都记录在上面。但是同时我的google日历却能访问，百思不得其解，抓包就看到服务器不可用，没什么其他值得注意的内容，但是换个计算机就能访问，奇怪死了，检查了arp，正常，检查了hosts文件，正常，机器是XP补丁全＋360＋NOD32＋彩影ARP防火墙＋Windows防火墙。今天忽然想起来，ping了一下：
 
C:/>ping docs.google.comPinging writely.l.google.com [72.14.203.101] with 32 bytes of data:Request timed out.
 
发现域名被重定向了，我在其他机器试验了一下，docs的地址应该是209.85.143.100，但是直接访问这个地址却去了google首页。点击链接提示请求的网页无效。
```

# TD告诉我The RPC server is unavailable

2009-02-18 11:30:00

```
TestDirector作为业界最差的bug系统，TD很敬业的定期出现各种各样的错误。最常见的就是不支持你的浏览器、IE死掉或者提示The RPC server is unavailable。
 
首先，身为一个bug管理系统，TD只能安装在Windows主机上，这我能忍，但是同时TD不支持IE以外的浏览器，也就是说，我不能在其他操作系统访问到TD，我晕。而且不支持IE6以上版本的浏览器，如果想在高于IE6的浏览器中使用，需要首先修改TD中的一个htm文件，在里面增加版本判断或者干脆去掉那些毫无用处的代码。
对于IE被TD干掉一案，最初解决问题的办法很简单，重启TD服务就行了，但是TD的服务真的很难找，作为一个商业软件，它的开发团队明显不入流，服务名字完全没有规律，其中一个叫
Advanced TestDirector StartStop Service
还有一个叫
Send All Qualified App
我记得还有一个，没找到。都重启一遍，一般就好了。
 
后来，问题越出越频繁，重启服务也不能解决问题了，这时重启计算机，就好了。
 
昨天，我对系统做了加固，配置了一些安全策略，这时TD彻底瘫痪了，访问的时候永远在提示
The RPC server is unavailable
这提示本来眼熟，但这次怎么重启机器都不能恢复了。试图启动TDChecker，失败，提示必须用administrator登录，我晕，我做了重命名管理员账号的安全策略，TD你是不是弱智？你管理你的bug，你管我用谁登录系统？几经试验，发现使用C:/Inetpub/TDBIN/Apps下的ChangeRunAsUser.exe可以重新设定TD绑定的用户名和密码，TD是要保存你主机的管理员密码的，每次修改密码需要重新进行设定，TD再发展发展，可以成间谍软件了。
 
TD好用，在于它把需求，测试和bug管理结合了起来，但从纯软件的角度，这绝对是一个垃圾产品。
```

# bug是怎样炼成的

2008-10-24 10:44:00

```
 我很遗憾，做软件做了这么多年，思想还是停留在代码层次上，从来没有去提高自己。
近期的代码维护工作中碰到的问题，记录。

一条导致程序崩溃的代码：
unsigned long   lFeedbacktype_id;
语句本身没有问题，关键是它出现在哪。
昨天开始，A系统的C后台程序忽然崩溃，怎么也启动不了，错误提示是：

SQL Error! SQLSTATE = 07006 Native err = 0 msg = [Oracle][ODBC]Restricted data type attribute violation.
百思不得其解，过去好好的怎么今天忽然不行了，后来尝试了删除所有相关表中的数据，程序正常了，插入了今天的数据，还是出错，导出数据查看，似乎看不出异常。试验了一下，发现如果把其中两个值为－1的字段改为0，程序就正常了。
查看对应的DTL类，发现这些出错的字段都是unsigned long类型的，按说unsigned long和long是同样长度的，用哪个都不会出错，肯定是DTL库的内部对绑定的类型做了很严格的处理，如果声明的类型和数据库中的值不符合则会抛出异常。尝试把类型修改为：
long   lFeedbacktype_id;
问题解决。看来数据库中中的number类型，在DTL中应该使用long类型来绑定。这就是C程序员喜欢使用unsigned long来声明所有的整形变量所带来的恶果。
我目前维护这个项目的代码很有意思，其腐烂程度在我的工作历史中至少可以排名第二，我会慢慢把这些有意思的事情都记录下来。目前程序中所有绑定number字段的类成员都是使用的unsigned long，也就是说，所有的这些字段只要有负数出现，都会导致程序崩溃，真懒得去改。
环境：Oracle9i、ODBC、VC6、DTL
```

# [RDP]A glyph is a bitmap representation of a character

2008-08-08 18:25:00

```
关于RDP中的文本是如何取出的,一直不得其要领,在MSDN上看到的一句有关的话RDP text is displayed by using glyph caching. Almost immediately, the
client builds up the required set of glyphs, and the server needs only
transmit a short hash value to display the text.可能有关的代码:#define DO_GLYPH(ttext,idx) /{/  glyph = cache_get_font (font, ttext[idx]);/  if (!(flags & TEXT2_IMPLICIT_X))/  {/    xyoffset = ttext[++idx];/    if ((xyoffset & 0x80))/    {/      if (flags & TEXT2_VERTICAL)/        y += ttext[idx+1] | (ttext[idx+2] << 8);/      else/        x += ttext[idx+1] | (ttext[idx+2] << 8);/      idx += 2;/    }/    else/    {/      if (flags & TEXT2_VERTICAL)/        y += xyoffset;/      else/        x += xyoffset;/    }/  }/  if (glyph != NULL)/  {/    x1 = x + glyph->offset;/    y1 = y + glyph->baseline;/    XSetStipple(g_display, g_gc, (Pixmap) glyph->pixmap);/    XSetTSOrigin(g_display, g_gc, x1, y1);/    FILL_RECTANGLE_BACKSTORE(x1, y1, glyph->width, glyph->height);/    if (flags & TEXT2_IMPLICIT_X)/      x += glyph->width;/  }/}然后,又找到了一处:4 Rather than using font negotiation, RDP implements a glyph
and fragment caching mechanism. A glyph is a bitmap representation of a
character and its font information. For example, the character "A" in
Times New Roman is represented by a different glyph than the character
"A" in Arial. The use of glyphs allows characters to be displayed
precisely regardless of the client operating systems and the locally
installed fonts. A string of glyphs is called a 'fragment'. Because
glyphs and fragments are cached locally at the client, the server
improves bandwidth utilization by not resending the same glyphs.
Instead, it tells the client to reuse a cached glyph or fragment.字符串实际传递的还是字型的点阵,点阵实际是一个位图,也就是说,字符串的内容是无法简单识别的.文档中也说明了,文本所以不直接传递纯文本,第一是不安全,文本中可能包含敏感信息而被黑客盗用.第二是使用位图点阵,可以保证不同的操作系统可以得到相同的显示结果.看来,取得文本内容的努力算是失败了?
```

# [Snort]加了rule文件之后得到Unknown rule type: portvar错误

2008-07-30 12:03:00

```
加了一些从网上下载的最新rules，并修改了对应的配置，结果报错：[root@localhost snort]# snort -A full -s -c /etc/snort/etc/snort.conf -i eth0 Running in IDS mode        --== Initializing Snort ==--Initializing Output Plugins!Var 'any_ADDRESS' defined, value len = 15 chars, value = 0.0.0.0/0.0.0.0Var 'lo_ADDRESS' defined, value len = 19 chars, value = 127.0.0.0/255.0.0.0Initializing Preprocessors!Initializing Plug-ins!Parsing Rules file /etc/snort/etc/snort.conf+++++++++++++++++++++++++++++++++++++++++++++++++++Initializing rule chains...Var 'HOME_NET' defined, value len = 3 chars, value = anyVar 'EXTERNAL_NET' defined, value len = 3 chars, value = anyVar 'DNS_SERVERS' defined, value len = 3 chars, value = anyVar 'SMTP_SERVERS' defined, value len = 3 chars, value = anyVar 'HTTP_SERVERS' defined, value len = 3 chars, value = anyVar 'SQL_SERVERS' defined, value len = 3 chars, value = anyVar 'TELNET_SERVERS' defined, value len = 3 chars, value = anyVar 'SNMP_SERVERS' defined, value len = 3 chars, value = anyVar 'FTP_SERVERS' defined, value len = 3 chars, value = anyVar 'SSH_SERVERS' defined, value len = 3 chars, value = anyVar 'POP_SERVERS' defined, value len = 3 chars, value = anyVar 'IMAP_SERVERS' defined, value len = 3 chars, value = anyVar 'RPC_SERVERS' defined, value len = 3 chars, value = anyVar 'WWW_SERVERS' defined, value len = 3 chars, value = anyVar 'AIM_SERVERS' defined, value len = 185 chars   [64.12.24.0/23,64.12.28.0/23,64.12.161.0/24,64.12.163.0/24,64.12.200.0/24,205.188.3.0/24,205.188.5.0/24,205.188.7.0/24,205.188.9   .0/24,205.188.153.0/24,205.188.179.0/24,205.188.248.0/24]ERROR: /etc/snort/etc/snort.conf(123) => Unknown rule type: portvarFatal Error, Quitting..网上查询说是路径设置的问题。我的路径设置如下：var RULE_PATH /etc/snort/rules之前是./rules，两种情况都是出上面的错误。
```

# 两个极端可以得到同样的效果

2008-07-10 14:15:00

```
从集团查询的SQL语句我们可以看出，两个极端可以得到同样的效果
```

# 一个SQL

2008-07-09 14:52:00

```
项目中的一段SQL其实，这个项目中充满了超长的SQL，最长的一个竟然在代码中写了二百多行SELECT  * FROM (SELECT * FROM APPEAL,REGION,HANDLESTATE,FEEDBACKTYPE WHERE APPEAL.APPEAL_REGION_ID =REGION.REGION_ID(+) AND APPEAL.APPEAL_HANDLESTATE_ID = HANDLESTATE.HANDLESTATE_ID(+) AND APPEAL.APPEAL_FEEDBACKTYPE_ID = FEEDBACKTYPE.FEEDBACKTYPE_ID(+) AND APPEAL_ID IN (SELECT DISTINCT APPEAL_ID FROM APPEALTOORIGIN WHERE APPEAL_ORIGIN_ID IN (SELECT APPEAL_ORIGIN_ID FROM APPEAL_ORIGIN WHERE 1 = 1 AND APPEAL_SOURCE_ID=2 AND APPEAL_EMAIL LIKE '%rebound@ns.net%' )) AND  1 = 1 AND APPEAL_HANDLESTATE_ID=1 AND 1=1 AND APPEAL_LASTTIME>=1214841600 AND  APPEAL_LASTTIME<=1217519999 ) WHERE (ROWID IN (SELECT rid FROM (SELECT rownum rno, rid FROM (SELECT rowid rid FROM (SELECT * FROM APPEAL,REGION,HANDLESTATE,FEEDBACKTYPE WHERE APPEAL.APPEAL_REGION_ID =REGION.REGION_ID(+) AND APPEAL.APPEAL_HANDLESTATE_ID = HANDLESTATE.HANDLESTATE_ID(+) AND APPEAL.APPEAL_FEEDBACKTYPE_ID = FEEDBACKTYPE.FEEDBACKTYPE_ID(+) AND APPEAL_ID IN (SELECT DISTINCT APPEAL_ID FROM APPEALTOORIGIN WHERE APPEAL_ORIGIN_ID IN (SELECT APPEAL_ORIGIN_ID FROM APPEAL_ORIGIN WHERE 1 = 1 AND APPEAL_SOURCE_ID=2 AND APPEAL_EMAIL LIKE '%rebound@ns.net%' )) AND  1 = 1 AND APPEAL_HANDLESTATE_ID=1 AND 1=1 AND APPEAL_LASTTIME>=1214841600 AND  APPEAL_LASTTIME<=1217519999 ) ORDER BY APPEAL_COUNT DESC) WHERE rownum <= 100) WHERE rno >= 1)) ORDER BY APPEAL_COUNT DESC我想知道的是，这样的SQL这个人是怎么写出来的？
```

# 一段代码

2008-07-08 10:45:00

```
项目中的一段代码，不知道是谁写的：

String sql = "UPDATE SAFE SET SAFE_IP_TYPE_ID=?,SAFE_FEEDBACKTYPE_ID=?,SAFE_USERNAME=?,SAFE_PHONE=?,SAFE_ACCOUNT=?,SAFE_REMARK=?,SAFE_HANDLER=?,SAFE_HANDLESTATE_ID=?,SAFE_HANDLE_FLAG=?,SAFE_RESULT=?,safe_ip_dns=?,safe_priority_id=?,safe_count=?,safe_failed_times= ?,safe.safe_review_count = ? ,safe.safe_lasttime=? ,safe.SAFE_BETIMES=? ,safe_change_count=? WHERE SAFE_ID = ?";
Object[] param = { "long",
		String.valueOf(safe.getSafe_ip_type_id()), "long",
		String.valueOf(safe.getSafe_feedbacktype_id()), "string",
		String.valueOf(safe.getSafe_username()), "string",
		String.valueOf(safe.getSafe_phone()), "string",
		String.valueOf(safe.getSafe_account()), "string",
		String.valueOf(safe.getSafe_remark()), "string",
		String.valueOf(safe.getSafe_handler()), "long",
		String.valueOf(safe.getSafe_handlestate_id()), "long",
		String.valueOf(safe.getSafe_handle_flag()), "string",
		String.valueOf(safe.getSafe_result()), "string",
		String.valueOf(safe.getSafe_ip_dns()), "long",
		String.valueOf(safe.getSafe_priority_id()), "long",
		String.valueOf(safe.getSafe_count()), "long",
		String.valueOf(safe.getSafe_failed_times()), "long",
		String.valueOf(safe.getSafe_review_count()), "long",
		String.valueOf(safe.getSafe_lasttime().getTime() / 1000), "long",
		String.valueOf(safe.getSafe_betimes()), "long",
		String.valueOf(safe.getSafe_id()),"long",String.valueOf(safe.getSafe_Chang_count())
		};      
DataBaseUtil.executeUpdate(sql, param)

同事在维护这段代码的时候出了错，他在SQL中加了一个字段，并且在Object[] param中加了参数的赋值： String.valueOf(safe.getSafe_count()), "long" 
按说没问题的。  
仔细一看，晕倒，原来Object[] param的格式要求是
 "类型","值" 
而同事按照上面代码的格式写成了
"值"，"类型"。 
原来很搞笑的原作者，在第一行写了一个"类型"后，下面的行都按照"值","(下一个参数的)类型"的格式去写， 这样，原来的
 "类型","值", 
"类型","值",
 格式就看起来变成了
 "值","类型",
 "值","类型",  
这么眩晕的创意型代码不知道是哪位仁兄的大作啊，好久没欣赏过这样的代码了，实在是有创意啊！
```

# 暂时放弃VC2008

2008-06-30 11:06:00

```
对2008忍无可忍，决定暂时放弃它，回到VC6＋VC2003的时代。

最主要的问题是CPU100%的问题，伟大的IntelliSense，每次一打开项目，他就要占100%的CPU，我只能在一旁老老实实等着他老人家工作完，等个一两分钟那算你幸运，等个七八分钟再也不响应了，也不是什么新鲜事。网上查到只要把<VS root path>/VC/vcpackages/feacp.dll改名就行了，我试验了，有效，关键是我再也无法转到函数定义，也没法查看函数参数了。VC是一个毫无进取精神的软件，到了2008，类的函数列表还是经常出不来，没有VA简直没法干活，我装了新版VA，发现已经有了一些重构的功能了，微软的VS开发者就不惭愧么？（或者是微软根本不想进化VC了）   


还有就是没完没了的bug，发现2003里的bug，基本被2008光荣继承了。而2003的不足，2008虽然也有一些改进，比如2003那个该死的ICON编辑器，只是，基本每个改进之处都有bug...我无语了，这样的东西是不是根本没经过测试就上市了。美国版本的《仙剑二》？ 

还有64位的问题，暂时用不上，就别跟我这碍事了，我这都_w64指针截断了：
 warning C4311: “类型转换” : 从“dll::SMSMSG *__w64 ”到“DWORD”的指针截断
算了，您还是回光盘包里度假去吧。
```

# 如何不用额外的变量交换两个变量的值

2008-06-25 18:32:00

```
同事买了本《编程之美》，然后就给我出的一个算法题，非常的有意思。已知：a=xb=y问：如何不用额外的变量交换a和b的值？答案是：a=a+bb=a-ba=a-b太有意思了！
```

# STL迭代器：循环中删除

2008-06-16 16:16:00

```
直接删除肯定不行，不然我的程序也不会崩溃了。
首先尝试了下面的方法，很笨
IEnumCbCmdResponseFuncs::iterator itor;

for (itor=m_Funcs.begin();itor!=m_Funcs.end();itor++)

{

	ResponseFunc pFunc = *itor;

	if (!pFunc.enable)

	{

		m_Funcs.erase(itor);

		itor=m_Funcs.begin();

		if (itor==m_Funcs.end())

		{

			break;

		}

		continue;

	}

}
然后知道了下面的方法
IEnumCbCmdResponseFuncs::iterator itor;

for (itor=m_Funcs.begin();itor!=m_Funcs.end();)

{

	ResponseFunc pFunc = *itor;

	if (!pFunc.enable)

	{

		m_Funcs.erase(itor++); // 删除的是itor的复本（参考STL源码++的重载）

		continue;

	}

	++itor;

}
```

# 写文件速度测试

2008-05-27 16:33:00

```
测试了不同方法写文件的时间，测试环境是IBM T42：代码一：
    char *data=new char[1024*1024];    int t0 = GetTickCount();    FILE *pFile = NULL;        pFile = fopen("D:/test1MB_C.dat", "a+");    fwrite(data, 1024*1024,1,pFile);    fclose(pFile);    int t1 = GetTickCount();    delete[] data;    data = NULL;    char szText[32];    sprintf(szText, "use %d second(%d 毫秒).", (t1-t0)/1000, t1-t0 );    this->SetWindowText(szText);

写1MB数据到磁盘，只计算文件操作部分的时间，执行时间是50毫秒。代码二：
    char *data=new char[1024*1024];    int t0 = GetTickCount();    std::fstream fsFile("D:/test1MB.dat" , std::ios::out | std::ios::binary);        fsFile.write( data,  1024*1024 );         fsFile.close();    int t1 = GetTickCount();    delete[] data;    data = NULL;    char szText[32];    sprintf(szText, "use %d second(%d 毫秒).", (t1-t0)/1000, t1-t0 );    this->SetWindowText(szText);

类似代码一，但是用的是fstream类来写文件，执行时间是300毫秒。对比了Java写文件所需要的时间，同环境Java写1MB数据的耗时是94毫秒，比使用fstream的速度快，比fwrite的方法慢。不过java的速度还是超过我的想象。
```

# C++的Format

2008-05-21 17:01:00

```
他们管这个叫C++的format，其实这种方法也比较诡异
std::ostringstream strSQLS;strSQLS << "WHERE FRAMEIP = "            <<szIp            <<" and LOGINTIME<="            <<time1            <<" AND LOGOUTTIME>="            <<time1            ;

好处是不用关心数据的类型了，缺点是原始串不直观。
```

# 是STL的错误吗？（续）

2008-05-21 15:12:00

```
特定情况下，以下的写法导致最后一个单引号没加上(display为std::string对象)：写法1：
string strSQL;strSQL = "WHERE APPEAL_DISPLAY='";strSQL.append(display);strSQL.append(" ' "); 

写法2：
string strSQL = "WHERE  APPEAL_DISPLAY='" + display + " ' ";

写法3：
string strSQL = "WHERE  APPEAL_DISPLAY='" + display + " /' ";

以下写法不出此问题：
char szSQL[256] = {0};string strSQL;sprintf(szSQL, "WHERE  APPEAL_DISPLAY='%s'", display.c_str() );strSQL = szSQL;

调试之前执行了Clean+Rebuild，VC6，操作系统是Win2003，但是另外写一个工程运行上述代码就不出错。出错的时候display的内存情况：
02083E31  67 7A 44 53 4C 38 37 32 35 36 35 31 31 00 00  gzDSL87256511..   

strSQL的内存：
02080A61  57 48 45 52 45 20 41 50 50 45 41 4C 5F 44 49  WHERE APPEAL_DI02080A70  53 50 4C 41 59 3D 27 67 7A 44 53 4C 38 37 32  SPLAY='gzDSL87202080A7F  35 36 35 31 31 00 00 00 00 00 00 00 00 00 00  56511.......... 

又经过试验，发现display.size() 为256 ！所以想象可能还是类似上次的包含/0的问题。追查display的来源如下：display = CTAppeal.GetExtenNum();按想象string不能保存包含/0的字符串，再次测试：
经过测试：const std::string display="sgsg8176216/0/0/0/0";int a=display.size();

a==11string是不会被直接赋值为一个包含/0的字符串的。但是，这里有个问题，就是这样赋值的话应该是被编译器给截断的。所以内存赋值可能string实际可以支持。GetExtenNum()是输出数据库字段的值然后返回，其间也是用string保存数据的，dtl库的内部实现我并不了解，但推测应该还是字符串被赋了包含零的值。写测试程序如下：
string str = "123";str.append("/ 0/ 0/ 0",3);str.append("E");string::size_type srclen=str.size();

seclen为7，内存情况如下：
00E653D9  31 32 33 00 00 00 45 00 CD CD CD CD  123...E.屯屯

赋值成功。 我的程序因为那个字段的值包含/0，并且保存在了string中，所以在拼SQL的时候，导致单引号拼接失败，最终导致SQL执行失败。结论：使用string的时候要格外当心/0的问题。恶意使用者可通过向数据库提交包含/0的字符串来使后台程序崩溃（斜杠零攻击）。
```

# [OCI] OCI基础学习笔记：Select的方法

2008-05-13 18:53:00

```
#include   <oci.h>       OCIEnv   *m_pOCIEnv;       OCIError   *m_pOCIError;       OCISvcCtx   *m_pOCISvcCtx;       OCIStmt   *m_Insertp;       OCIStmt   *m_pOCIStmtSelectR;       OCIBind   *m_Bndhp;    登录：     char   szUserID[STRING_LEN];       char   szPassWord[STRING_LEN];       char   szServerName[STRING_LEN];        (void) OCIEnvCreate(&m_pOCIEnv, OCI_THREADED, (dvoid *)0,                                 0, 0, 0, (size_t) 0, (dvoid **)0);      OCIHandleAlloc((dvoid   *)m_pOCIEnv,   (dvoid   **)&m_pOCIError,   OCI_HTYPE_ERROR,   (size_t)0,   (dvoid   **)0);        strcpy(szServerName,   "Ora_servername");       strcpy(szUserID,   "username");       strcpy(szPassWord,   "password");        ProcessError(m_pOCIError,           nRetCode = OCILogon(m_pOCIEnv,   m_pOCIError,   &m_pOCISvcCtx,           (unsigned   char   *)szUserID,   strlen(szUserID),           (unsigned   char   *)szPassWord   ,   strlen(szPassWord),           (unsigned   char   *)szServerName,   strlen(szServerName)           ));       if (nRetCode != OCI_SUCCESS)     {         return -1;     }  一个Select查询的初始化：     const   char   *pszSelectSql  = NULL;      pszSelectSql   =   "select OBJECT from ORIGIN WHERE HANDLE_FLAG=0 AND  rownum<5";          OCIHandleAlloc((dvoid   *)m_pOCIEnv,   (dvoid   **)&m_pOCIStmtSelectR,   OCI_HTYPE_STMT,   (size_t)0,   (dvoid   **)0);        OCIStmtPrepare(m_pOCIStmtSelectR,   m_pOCIError,   (text   *)pszSelectSql,   (ub4)strlen(pszSelectSql),                 (ub4)OCI_NTV_SYNTAX,   (ub4)OCI_DEFAULT)  ;                  OCIDefine *m_pOCIDefSelect = NULL;        ProcessError(m_pOCIError, OCIDefineByPos(m_pOCIStmtSelectR, &m_pOCIDefSelect, m_pOCIError, 1, (dvoid *) &lObject,                  (sword) sizeof(double), SQLT_FLT, (dvoid *) 0, (ub2 *)0,                  (ub2 *)0, OCI_DEFAULT));  执行查询并取得记录集：     OCIStmtExecute(m_pOCISvcCtx,   m_pOCIStmtSelectR,   m_pOCIError,   (ub4)1,   (ub4)0,                      (CONST   OCISnapshot   *)NULL,   (OCISnapshot   *)NULL,   OCI_DEFAULT);      while(errno==OCI_SUCCESS_WITH_INFO || errno==OCI_SUCCESS)     {         printf("ip=%f,%s/r/n", lObject, "");         errno = OCIStmtFetch ( m_pOCIStmtSelectR, m_pOCIError, 1, OCI_FETCH_NEXT, OCI_DEFAULT);     }  原理是首先初始化OCI环境，分配表达式句柄，然后用OCIDefineByPos绑定变量，第四个参数是从1开始的查询结果对应的字段序号，最后用OCIStmtExecute执行查询，并调用OCIStmtFetch遍历结果集，没有结果会得到OCI_NO_DATA
```

# VC90的exe换了环境不能运行

2008-03-06 14:07:00

```
VC90编译的exe本机正常，连同mfc90.dll、msvcr90.dll、msvcp90.dll一起拷贝到另外机器上，执行出现This application has failed to start because the application configuration is incorrect. Reinstalling the application may fix the problem 错误提示。使用depends查看，不缺少DLL。改用静态链接MFC可解决此问题，但是问题产生的原因未知。
```

# 64位时代来临了，升级到VC2008一定要多加小心！

2008-03-05 16:39:00

```
今天碰到如下代码出现逻辑错误：for(int nNo=1;nNo<=8;nNo++){    char szSQL[256]={0};    time_t mstime;     time(&mstime);    sprintf(szSQL, "update status set status='%s', mstime=%d where id=%d",strStatus[nNo].c_str(), mstime , nNo);    pConn->Execute(szSQL);}每次执行，条件都是where id=0，百思不得其解，查看MSDN，发现原来time_t和time的内部实现已经变化，需要改变代码为：__time32_t mstime; _time32(&mstime);sprintf(szSQL, "mstime=%d... "..,mstime, nNo);或者需要定义这个宏：_USE_32BIT_TIME_T 才可以，这个宏要写到项目属性里，或者stdafx的第一行，不然会出现：.../VC/INCLUDE/sys/stat.inl(44) : error C2466: cannot allocate an array of constant size 0错误。time_t和time的默认已经变为64位实现了。这个会导致升级到2008的VC代码产生很大的隐患，因为编译不会出错，但是执行结果却逻辑错误。看来升级到 VC2008的一定要注意，不然真的很危险。MSDN:time_t (__int64 or long integer) Represents time values in mktime, time, ctime, _ctime32, _ctime64, _wctime, _wctime32, _wctime64, ctime_s, _ctime32_s, _ctime64_s, _wctime_s, _wctime32_s, _wctime64_s, ctime, _ctime32, _ctime64, _wctime, _wctime32, _wctime64 and gmtime, _gmtime32, _gmtime64. If _USE_32BIT_TIME_T is defined, time_t is a long integer. If not defined, it is a 64-bit integer.
```

# 升级到VC 2008之后变体类型问题

2008-02-28 10:46:00

```
从VC6或者VC2003(VC7.1)升级到VC2008（VC9.0）之后，很多的程序不能编译了，很多能编译的运行的不对了。比如:过去的ADO数据库访问一切正常，到了2008里虽然可以编译，但是取出的整数值都是0，跟踪发现，代码中的一段:    _variant_t aa = GetValueByField(strFName);        if( aa.vt == VT_NULL )        return 0;        return aa.intVal;aa的值正确，但是aa.intVal的值是0，咨询同事后得知这里应该写为        return int(aa); 修改后在2008也正常了。可能变体类型的定义在2008里发生了变化，所以过去那种比较猛的直接访问数据成员的方法失效了。还比如一个COM组件的调用程序，过去一直正常，2008里不能编译了，出错在[ module(DLL, name="Fst", uuid="{2726C85B-BF30-4b4b-8529-289D3E05CE4B}") ];修改为[ module(type=dll, name="DllFst", uuid="{2726C85B-BF30-4b4b-8529-289D3E05CE4B}") ];即可编译通过，这里是因为2008里的写法要求更严格了。还有类似的错误：__hook(&IFstEvents::OnRegChange, pSource, OnRegChange);需要修改为：__hook(&IFstEvents::OnRegChange, pSource, &CMsg::OnRegChange);类成员函数需要加上类名和取地址符（是编译器告诉我要这样写的）。还好，多数程序最终还是通过了编译，希望他们也能正确的运行。
```

# 是STL的错误吗？

2008-02-26 18:59:00

```
碰到很奇怪的问题string::size_type nlen = str.size();   // 得到1108str.erase(pos, 3);这句出错，跟踪进去，是_Split();里面得到了错误的_Len导致的。assign(_Temp);里面的_Tr::length(_S)得到了一个788，而之前调用str.size()得到的是1108，这就导致后面_Tr::move(_Ptr + _P0, _Ptr + _P0 + _M,                _Len - _P0 - _M)的时候_Len - _P0 - _M的值已经为负数，经过仔细研究，发现这个字符串是一个包含/0的长字符串（其值是由DTL库从Oracle数据库中取出），1108是它真正的长度，788正好是/0所在的位置，就是说，对于这种数据，不能用string类来处理。但是，随后我又写了一个试验程序：     string str = "测试/0;/r/nA;/r/n中文中文;/r/n<E>/r/n";     string::size_type srclen=str.size();srclen得到4这又说明size()方法是能处理/0的。又是一个百思不得其解。原始串如下：00E79C61  52 65 63 65 69 76 65 64 3A 20 66 72 6F 6D  Received: from00E79C6F  20 31 32 36 2E 63 6F 6D 20 28 5B 31 32 35   126.com ([12500E79C7D  2E 39 31 2E 31 34 31 2E 32 31 36 5D 29 0D  .91.141.216]).00E79C8B  0A 09 62 79 20 6E 61 6E 6F 70 72 6F 62 65  .    by nanoprobe00E79C99  73 2E 63 6F 6D 20 28 38 2E 31 33 2E 31 2F  s.com (8.13.1/00E79CA7  38 2E 31 33 2E 31 29 20 77 69 74 68 20 45  8.13.1) with E00E79CB5  53 4D 54 50 20 69 64 20 6D 30 44 36 78 48  SMTP id m0D6xH00E79CC3  50 76 30 30 38 38 36 37 0D 0A 09 66 6F 72  Pv008867..    for00E79CD1  20 3C 78 3E 3B 20 53 75 6E 2C 20 31 33 20   <x>; Sun, 13 00E79CDF  4A 61 6E 20 32 30 30 38 20 30 31 3A 35 39  Jan 2008 01:5900E79CED  3A 32 32 20 2D 30 35 30 30 0D 0A 4D 65 73  :22 -0500..Mes00E79CFB  73 61 67 65 2D 49 64 3A 20 3C 32 30 30 38  sage-Id: <200800E79D09  5F 5F 5F 5F 5F 5F 5F 5F 5F 5F 5F 5F 5F 5F  ______________00E79D17  5F 5F 5F 5F 5F 38 38 36 37 40 6E 61 6E 6F  _____8867@nano00E79D25  70 72 6F 62 65 73 2E 63 6F 6D 3E 0D 0A 58  probes.com>..X00E79D33  2D 4F 72 69 67 3A 20 5B 31 32 35 2E 39 31  -Orig: [125.9100E79D41  2E 31 34 31 2E 32 31 36 5D 0D 0A 58 2D 41  .141.216]..X-A00E79D4F  75 74 68 65 6E 74 69 63 61 74 69 6F 6E 2D  uthentication-00E79D5D  57 61 72 6E 69 6E 67 3A 20 6E 61 6E 6F 70  Warning: nanop00E79D6B  72 6F 62 65 73 2E 63 6F 6D 3A 20 6E 61 6E  robes.com: nan00E79D79  6F 70 72 6F 62 20 6F 77 6E 65 64 20 70 72  oprob owned pr00E79D87  6F 63 65 73 73 20 64 6F 69 6E 67 20 2D 62  ocess doing -b00E79D95  73 0D 0A 46 72 6F 6D 3A 20 3D 3F 47 42 32  s..From: =?GB200E79DA3  33 31 32 3F 42 3F 77 4F 37 50 79 4D 6E 36  312?B?wO7PyMn600E79DB1  3F 3D 20 3C 6C 62 67 5F 35 32 30 40 31 32  ?= <lbg_520@1200E79DBF  36 2E 63 6F 6D 3E 0D 0A 53 75 62 6A 65 63  6.com>..Subjec00E79DCD  74 3A 20 3D 3F 47 42 32 33 31 32 3F 42 3F  t: =?GB2312?B?00E79DDB  79 63 2B 36 6F 37 76 6A 77 66 71 37 34 62  yc+6o7vjwfq74b00E79DE9  7A 47 79 73 4C 4F 38 63 76 35 3F 3D 0D 0A  zGysLO8cv5?=..00E79DF7  54 6F 3A 20 78 0D 0A 43 6F 6E 74 65 6E 74  To: x..Content00E79E05  2D 54 79 70 65 3A 20 74 65 78 74 2F 70 6C  -Type: text/pl00E79E13  61 69 6E 3B 63 68 61 72 73 65 74 3D 22 47  ain;charset="G00E79E21  42 32 33 31 32 22 0D 0A 52 65 70 6C 79 2D  B2312"..Reply-00E79E2F  54 6F 3A 20 6C 62 67 5F 35 32 30 40 31 32  To: lbg_520@1200E79E3D  36 2E 63 6F 6D 0D 0A 44 61 74 65 3A 20 53  6.com..Date: S00E79E4B  75 6E 2C 20 31 33 20 4A 61 6E 20 32 30 30  un, 13 Jan 20000E79E59  38 20 31 35 3A 30 33 3A 35 39 20 2B 30 38  8 15:03:59 +0800E79E67  30 30 0D 0A 58 2D 50 72 69 6F 72 69 74 79  00..X-Priority00E79E75  3A 20 33 0D 0A 58 2D 4D 61 69 6C 65 72 3A  : 3..X-Mailer:00E79E83  20 46 6F 78 4D 61 69 6C 20 34 2E 30 20 62   FoxMail 4.0 b00E79E91  65 74 61 20 32 20 5B 63 6E 5D 0D 0A 58 2D  eta 2 [cn]..X-00E79E9F  53 70 61 6D 43 6F 70 2D 43 68 65 63 6B 65  SpamCop-Checke00E79EAD  64 3A 20 36 36 2E 38 34 2E 32 32 2E 31 32  d: 66.84.22.1200E79EBB  36 20 31 32 35 2E 39 31 2E 31 34 31 2E 32  6 125.91.141.200E79EC9  31 36 20 0D 0A 0D 0A 0D 0A 20 20 20 20 20  16 ......     00E79ED7  20 20 20 20 20 20 20 20 20 20 20 20 20 20                00E79EE5  B4 FA 20 B0 EC 20 B7 A2 20 C6 B1 28 31 33  代 办 发 票(1300E79EF3  39 32 36 35 31 35 33 32 33 29 0D 0A 20 20  926515323)..  00E79F01  20 D3 C9 CE D2 CB F9 B4 FA B0 EC B8 F7 C0   由我所代办各.00E79F0F  E0 B7 A2 C6 B1 BF C9 CF ED CA DC B4 F3 B7  喾⑵笨上硎艽蠓00E79F1D  F9 B5 CD CB B0 3B 20 20 0D 0A 20 20 20 B4  退.;  ..   .00E79F2B  FA B0 EC B8 F7 B5 D8 B7 FE CE F1 C0 E0 28  旄鞯胤窭.(00E79F39  D7 C9 D1 AF B7 D1 2C D7 A1 CB DE B7 D1 2C  咨询费,住宿费,00E79F47  BB E1 CE F1 B7 D1 2C B9 E3 B8 E6 B7 D1 2C  会务费,广告费,00E79F55  B7 BF D7 E2 0D 0A B7 D1 29 A3 BB B9 A4 B3  房租..费)；工.00E79F63  CC C0 E0 28 D7 B0 E4 EA B7 D1 2C C0 CD CE  汤.(装潢费,劳.00E79F71  F1 B7 D1 2C 00 00 00 BD A8 D6 FE B0 B2 D7  穹.,...建筑安.00E79F7F  B0 29 BC B0 C9 CC C6 B7 A1 A2 C9 CC D2 B5  .)及商品、商业00E79F8D  A1 A2 B9 A4 0D 0A D2 B5 CF FA CA DB C0 E0  、工..业销售类00E79F9B  B5 C8 B7 A2 C6 B1 B0 B4 31 2E 35 25 CA D5  等发票按1.5%收00E79FA9  B7 D1 A3 AC CD AC CA B1 D3 D0 C8 AB B9 FA  费，同时有全国00E79FB7  B8 F7 B4 F3 B3 C7 CA D0 B9 AB CB BE B4 FA  各大城市公司代00E79FC5  0D 0A C0 ED B5 C4 C6 B1 BE DD 3B 0D 0A D4  ..理的票据;...00E79FD3  F6 D6 B5 CB B0 B0 B4 36 25 B4 FA BF AA 3B  鲋邓鞍.6%代开;00E79FE1  0D 0A 20 20 20 D0 C5 D3 FE B3 D0 C5 B5 3A  ..   信誉承诺:00E79FEF  CF C8 CE DE CC F5 BC FE BD BB BB F5 B8 F8  先无条件交货给00E79FFD  B9 F3 CB BE C8 B7 C8 CF BA F3 D4 D9 B8 B6  贵司确认后再付00E7A00B  BF EE 21 28 C4 FA CE DE D0 E8 0D 0A B3 D0  款!(您无需..承00E7A019  B5 A3 C8 CE BA CE BE AD BC C3 C9 CF B5 C4  担任何经济上的00E7A027  B7 E7 CF D5 29 0D 0A C1 AA 20 CF B5 20 C8  风险)..联 系 .00E7A035  CB 3A 20 C0 EE CF C8 C9 FA 20 20 20 20 20  .: 李先生     00E7A043  20 20 20 20 20 20 20 20 20 20 20 20 20 20                00E7A051  20 20 20 30 32 31 2D 33 31 32 36 32 33 33     021-312623300E7A05F  39 20 20 0D 0A CA D6 20 20 20 20 BB FA 3A  9  ..手    机:00E7A06D  20 31 33 39 32 36 35 31 35 33 32 33 0D 0A   13926515323..00E7A07B  0D 0A 20 20 20 20 20 20 20 20 20 20 20 20  ..            00E7A089  20 20 20 20 20 20 20 20 20 20 20 20 20 20                00E7A097  20 20 20 20 20 20 C9 CF BA A3 BB E3 C1 FA        上海汇龙00E7A0A5  BB E1 BC C6 CA C2 CE F1 CB F9 0D 0A 0D 0A  会计事务所....00E7A0B3  0D 0A 00 CD CD CD CD CD CD CD CD CD CD CD  ...屯屯屯屯屯.00E7A0C1  FD FD FD FD F0 AD BA 0D F0 AD BA 0D F0 AD  瓠..瓠..瓠00E7A0CF  BA AB AB AB AB AB AB AB AB 00 00 00 00 00  韩......00E7A0DD  00 00 00 0A 00 95 00 EE 04 EE 00 90 5D E7  ...........怾.
```

# 错误地正确运行着

2008-02-26 15:42:00

```
维护的代码中的一段，目的是删除字符串中分号后的回车符（删除“分号回车换行”的组合），之前一直正确的运行，这次出了问题，跟踪到这里：
string::size_type pos=0;       while( (pos=str.find("; / r / n", pos)) != string::npos)...{    str.erase(pos, 3);    pos += 3;} 

(晕，CSDN的blog竟然不能输入/ r / n ，自动被翻译了，晕倒)猛的一看，就感觉这个pos+3似乎有逻辑问题，经过试验，确实不应该＋3，因为删除之后已经指向后面的字符串了，不需要＋3。由于实际环境中很少出现“分号回车换行”之后马上接着又有“分号回车换行的”，而且这种组合也一般不出现在字符串结尾，所以虽然代码有逻辑错误，但是却可以一直“正确”地运行，我们笑称这是"错误地正确运行着"
```

# 关于DTL库不能SELECT本地Oracle表的问题

2008-02-26 14:56:00

```
过去一直正常的代码，春节后忽然报告错误，连一个普通的Select操作都不能进行：Exception type: DBExceptionMethod: DBStmt::Fetch()Error Message: Unable to fetch statment "SELECT CONFIG_COUNT_MAX, CONFIG_SYSTEM_INFO FROM SYSCONFIG"SQL Errors:(0) SQL Error! SQLSTATE = 07006 Native err = 0 msg = [Oracle][ODBC]Restricted data type attribute violation. 还有的时候错误信息是Numberic value out of range.百思不得其解，春节前还好好的，代码没有变过，怎么忽然就不能运行了呢？首先考虑是不是防火墙的问题，关闭了防火墙试验不行，然后换了一台机器试验，也不行；然后试验更换Oracle客户端的版本，春节前是用的9i，现在用的是10g，卸载了10g重新装9i，却还是不行；然后考虑是不是操作系统的变化造成的，过去是Win2000，春节后重新装了WinXP，于是在虚拟机里重新安装了一个Win2000Server、重新安装VC6＋SP6试验，还是不行；对比两个数据库服务器的表结构，没有区别，数据内容虽然不同，但是似乎也没有异常的数据内容；尝试用ADO写了一个访问程序，结果运行通过，可以访问此数据库并且取出数据，莫非是DTL库出问题了？然后尝试本地又搭建了一个Oracle数据库服务器，导入数据，然后发现程序访问这个数据库还是出一样的错误。然后尝试连接远程的一个同样的Oracle数据库，结果竟然成功了，于是尝试重启本地Oracle服务，无效；重启本地Oracle服务器，无效；尝试导入远程数据到本地，程序不出错了。然后导回本地的错误数据，开始逐一将字段值设置为0试验是哪个字段出了问题，最后发现其中一个字段设置为0之后（之前的值是负数 -1），程序可以正确运行了。查看本地C代码中对应的部分，DTL类中的定义是unsigned long，而数据库中该字段的定义是Numberic，一般来说，C中对unsigned long 赋负数值是不会出错的（虽然逻辑上可能不是你需要的结果），看来DTL库的内容对此有某种处理在，如果赋值和定义不符，则代码抛出异常（First-chance exception in App.exe (KERNEL32.DLL): 0xEBAD562F: (no name).），由于本地程序的定义是从逻辑角度定义的，某些逻辑上不可能为负数的都被定义为unsigned long，而数据库中则统一都是Numberic类型的，这是一种不统一的情况，考虑如果修改代码工作量非常巨大，所以暂时不准备解决此问题，而由前台程序负责保证数据库不要出现异常值（负数）。整个除错过程历时三天多，眩晕～
```

# Linux主机加入WindowsAD域

2007-12-02 15:06:00

```
我什么都不懂，以下总结都是根据网上文章和咨询网友自己试验出来的，写的不对欢迎指教 。
AD活动目录：Windows2003 Server计算机名：c.tech.comIP：192.168.100.150
Linux：unbutu 6.10 LAMP ServerIP：192.168.100.98
首先，看看Linux能不能pingAD服务器，要用域名试验，如果ping不通，要先
vim /etc/network/interface
把AD的IP地址加到这个配置文件中的 dns-nameservers段中，如
 dns-nameservers 202.106.0.20 192.168.100.150
然后再试验ping就可以通了。
```

# pexpect学习（一）

2007-11-28 17:25:00

```
pexpect官方网站 http://pexpect.sourceforge.net/  
pexpect是一个可以模拟终端用户与系统的交互的Python库。
今天学习了一下，写了一个简单的试验程序在ubuntu上执行： from pexpect import * child = spawn ('bash') child.expect('[#/$] ', timeout=5) 
child.sendline('ls') child.expect('[#/$] ', timeout=5) print child.before 
child.sendline('ls -l') i = child.expect(['(?i)readme','(?i)etc', EOF, TIMEOUT]) if i==0:     print 'i==0 README'     child.sendline('ls /')     i = child.expect(['(?i)etc','(?i)readme',EOF, TIMEOUT])     if i==0:         print 'etc'     else:         print 'no etc.' elif i==1:     print 'i==1'     print 'etc' 
child.sendline('exit') print 'end.' 
首先执行一个bash，然后执行ls，看当前目录有没有readme文件(?i)代表不区分大小写，如果有，执行i==0分支，否则是o==1分 支，i==0分支中又执行了"ls /"，看根目录有没有etc或者readme，并显示结果，最后退出bash。 运行通过。 
 bash的情况比较简单，再试验一个稍微复杂一点的： def testSSH():     pwd = 'errpwd'     child = spawn ('ssh 192.168.1.1')     child.sendline(pwd)     i = 0     while i==0:         i = child.expect(['(?i)password', '[#/$] ' , EOF, TIMEOUT])         print child.before         print child.after         if i==1:             child.sendline('exit')         elif i==0:             pwd = 'rightpwd'             child.sendline(pwd) 
这里模拟了一个ssh登录的过程，首先我们尝试用一个错误的密码登录，ssh不会报错，而是继续出现password提示符，再得到这个expect之 后，我们再尝试正确的密码，成功后退出ssh，并跳出while循环，程序结束。
```

# Python调用C的DLL和VC调用有什么区别？

2007-11-21 18:50:00

```
 
 之前我被这个问题搞晕了，一个C的DLL，VC写了测试程序调用完全没问题，但是Python调用就失败，百思不得其解，DLL开发者也说别人调用都是好的，肯定是你调用的问题，我查啊查的也没有结果，后来有一天，终于无意中发现，我的VC测试程序中，习惯性的第一行写着

CoInitialize(NULL) ;

会不会是这个问题，忽然想起那个DLL内部是用到ADO的！试验之后，发现果然问题解决了，原来是没有初始化COM！为什么其他调用程序都正常？我对DLL开发者解释道，这只是一个巧合罢了，那些调用程序刚好由MFC框架自动执行了COM初始化，而在Python里，是不是有人帮你自己执行的。
经过协商，DLL提供者在接口内执行了CoInitialize(NULL)，问题解决。
```

# Python调用C的DLL

2007-09-26 11:36:00

```
最近研究这个，准备在新部门里大用Python了
首先用VC建立一个试验用的DLL。
假设函数的参数是这样的

typedef struct _TASK_PARAM...{    int    nTaskPriority;    int    nMaxNum;     CHAR   szContent[512];      _TASK_PARAM::_TASK_PARAM()    ...{        ZeroMemory(this, sizeof(*this));    }} TASK_PARAM, *PTASK_PARAM;typedef CONST TASK_PARAM*  PCTASK_PARAM;

函数如下：

extern "C" int Test(PCTASK_PARAM para)...{     printf ("nTaskPriority=%d, nMaxNum=%d, szContent=%s",para->nTaskPriority,para->nMaxNum,para->szContent); return para->nTaskPriority;}

Python里首先这样声明对应的对象：

class TASK_PARAM(Structure):    _fields_ = [ ("nTaskPriority", c_int),                ("nMaxNum", c_int),                ("szContent", c_char * 512)]

然后这样调用：

cdll.LoadLibrary("C:/tjDll.dll");para = TASK_PARAM();para.nTaskPriority = 1;para.nMaxNum = 2;para.szNotifyContent = '中文/0';print para.szNotifyContentcdll.tjDll.Test(byref(para));

 
如果VC的函数里要修改Python传入的参数，例如：

extern "C" int TestIntRef(int* para)...{    *para = *para + 1;    return *para;}

 
Python里就这么玩：

intPara = c_int(9)print cdll.tjDll.TestIntRef(byref(intPara));print intPara.value;

 对于这种要修改字符串的：

extern "C" int TestCharRef(char* para)...{    strcpy(para, "char* test.");    return 2;}

也不在话下：

szPara = create_string_buffer('/0' * 64)print cdll.tjDll.TestCharRef(byref(szPara));print szPara.value;

 
都是从Python的ctypes的教程看来的。之前要from ctypes import*，好玩
```

# web.py如何取得提交表单的内容

2007-09-21 15:02:00

```
 如何取得提交表单的内容？
如果提交的页面是类似下面

<textarea name="xml" cols="80" rows="20">

 在POST方法中使用web.input即可取得其值，举例如下：

 i = web.input()print i['xml'];# 或者print i.xml; 

如果提交的表单含有file类型的数据，可以得到控件的名字和文件的内容（但是通过本方法不能得到文件原始名称）
 
如果提交的file类型的表单，例如

<input name="filebin1" type="file" size="80" maxlength="80"> 

可以用如下方法取得提交的文件名

i = web.input(filebin1={})print i.filebin1.filename

用i.filebin1得到类似下面的数据对象
FieldStorage('filebin1', 'C://getcwd.txt', 'D://eclipse//workspace//jnitest//WEB-INF//classes')
用i.filebin1.value取得文件的内容，本例中C://getcwd.txt的内容是：D:/eclipse/workspace/jnitest/WEB-INF/classes
 转帖了一份在
http://groups.google.com/group/webpy/web/faqchinese
我建立了个中文FAQ ^_^
```

# [备忘录] JNI：Java和C++的互相调用

2007-08-21 16:46:00

```
Java-->C++方向：
首先，用native声明接口，这个接口是留给C++来实现的package com.hoker;public class IVCDll {    static    {        System.load( "IVCDll.so" );    }    public static native int initDll();}方法的名称和DLL导出函数的名称无关，可以随意写，加载的so文件是这个中间层接口生成的，而不是你实际要调用的DLL文件先用javac编译所有的java文件，然后按照package中指定的路径把class文件拷贝过去javac *.java mv -f *.class ./com/hoker/还可能要设置一下库的路径：export LD_LIBRARY_PATH=./然后用javah命令（在bin目录下执行） 
javah com.hoker.IVCDll -classpath ./
把生成的h文件在C里实现，字符串类型传递：jstring jstrRet = NULL;jstrRet = (*env)->NewStringUTF(env, (char *)szRet);然后编译：gcc -fPIC com_hoker_IVCDLL.c -l自己的库 -o IVCDLL.so -shared注意：自己的库的名字是libpub.so话，-l参数里只写pub就行了再写一个java的调用程序:package com.hoker;public class d{    public static void main(String[] args)    {         IVCDLL.initDLL();    }}编译后执行：java com.hoker.dC++-->java方向：
我们首先保存一个虚拟机的全局指针（声明为static JavaVM* Manager::m_pJvm[1] = {NULL}）

jint r = JNI_GetCreatedJavaVMs(&Manager::m_pJvm[0], 1, &s);

然后在要调用Java的地方（比如另外一个线程），先绑定到当前线程，再调用

JNIEnv *env = NULL;(Manager::m_pJvm[0])->AttachCurrentThread((void **)&env, NULL);jclass System = env->FindClass("com/hoker/IVCDll");jmethodID getP = env->GetStaticMethodID( System, "OnEvent",   "()I");env->CallStaticObjectMethod(System, getP);

GetStaticMethodID的最后一个参数是方法的签名，不知道怎么写的话在cmd里用javap -s 类名来查看一下就知道了
```

# 代码错位问题，注意QQ那个家伙

2007-06-23 19:16:00

```
用VC7.1(VisualStudio.Net 2003)写程序的注意了，如果代码是从QQ窗口里粘贴过来的，有可能导致断点调试的时候代码错误，而且怎么重新编译也不行，而且从代码编辑窗口里看不出任何问题，想解决很难。今天终于有了发现，如果代码是从QQ窗口粘贴过来的，就会这样，解决方法是记住哪里是粘贴的，全部剪切掉，粘贴到记事本里再全选复制粘贴回VC就好了。
后来经过试验，发现是QQ粘贴过来代码的每行结尾不是0D0A，而是0D0909，VS里不能显示这个字符，（也不会显示出乱码，所以我们也没法发现），并导致了以上的问题。 
```

# 数个cidaemon.exe占用100%CPU

2007-06-18 11:22:00

```
今日进程里忽然有数个cidaemon.exe占用大量CPU，每次都使用killex才能将其杀掉，今天google了一下，发现这个进程其实是Windows的索引服务，在
控制面板-管理工具-服务
中将其设置为停止+禁用，问题解决。
但是过去这个服务一直开着，不知道为什么没有出现过这个现象。 
```

# emule源代码研究

2007-06-17 18:13:00

```
刚看了一点。eMule-VeryCD-src-070418
资源IDD_STATISTICS 是那个双击状态栏出来的图表界面（图表做的不错哦，希望是个易用的东西）
图表控件的实现应该是class COScopeCtrl（eMule-VeryCD-src-070418/src/OScopeCtrl.h ）
应用的地方是CStatisticsDlg中的

COScopeCtrl m_DownloadOMeter,m_UploadOMeter,m_Statistics;

重绘的地方

void CStatisticsDlg::RepaintMeters() ...{    CString Buffer;    m_DownloadOMeter.SetBackgroundColor(thePrefs.GetStatsColor(0));    // Background    m_DownloadOMeter.SetGridColor(thePrefs.GetStatsColor(1));        // Grid    m_DownloadOMeter.SetPlotColor(thePrefs.GetStatsColor(4), 0);    // Download session    m_DownloadOMeter.SetPlotColor(thePrefs.GetStatsColor(3), 1);    // Download average    m_DownloadOMeter.SetPlotColor(thePrefs.GetStatsColor(2), 2);    // Download current
```

# 试用log4cxx

2007-06-08 13:03:00

```
很不稳定不知道为什么，经常什么日志都写不出来，今天又出现三个异常：
testlog.exe 中的 0x77e8bc81 处最可能的异常: 0x80004002: 不支持此接口 。testlog.exe 中的 0x77e8bc81 处最可能的异常: 0x80004002: 不支持此接口 。
testlog.exe 中的 0x77e8bc81 处最可能的异常: Microsoft C++ exception: log4cxx::helpers::ClassNotFoundException @ 0x0012e444 。
程序不崩溃，但是生成的log4j的日志文件是空，一句都没写进去，诡异死了。配置文件也没错啊。


<log4j:configuration xmlns:log4j="http://jakarta.apache.org/log4j/"> <appender name="NULL" class="org.apache.log4j.performance.NullAppender">  <layout class="org.apache.log4j.SimpleLayout"/> </appender> <appender name="soclog" class="org.jboss.logging.appender.DailyRollingFileAppender">  <errorHandler class="org.jboss.logging.util.OnlyOnceErrorHandler" /> <param name="File" value="log/test3.log" /> <param name="Append" value="false" /> <param name="DatePattern" value="'.'yyyy-MM-dd" /> <param name="MaxFileSize" value="1024KB" />  <param name="MaxBackupIndex" value="10" />  <layout class="org.apache.log4j.PatternLayout">  <param name="ConversionPattern" value="%d %%%c-%p[%t] %m%n" /> </layout> </appender>  <category name="SOCMC" additivity="true"> <priority value="DEBUG"/> </category>  <root>  <priority value="DEBUG" />  <appender-ref ref="soclog" /> </root> </log4j:configuration>



调用



log4cxx::xml::DOMConfigurator::configure(cfgFile.c_str());...LoggerPtr logger = Logger::getLogger(Log::m_MoudleName);...LOG4CXX_DEBUG(logger, log.c_str());

 
```

# CVS小技巧:忽略不需要的文件

2007-06-08 13:01:00

```
小技巧：右键某个CVS文件夹，CVS-首选项-忽略文件，输入*.opt *.ncb *.suo *.plg *.pch *.idb *.pdb *.scc *.obj Debug Release *.o *.bin *.out *.ilk *.aps debug release *.clw *.bak确定，这样以后添加所有内容的时候就会自动排除这些文件，再也不用自己手动去勾掉这些文件了，省事不少。 
```

# C#的DLL注册为COM，VB来调用

2007-06-08 13:00:00

```
非常实用的东西！过去知道这个方法的话可以解决多少问题啊
首先建立一个C#的DLL工程，写一个类


//Test.csnamespace Test...{public class MyTest...{public string Fun()...{return this.ToString();}}}


，编译
然后在cmd里执行VS的vsvars32.bat设置环境变量，然后执行


regasm cscomtest.dll /tlb:cscomtest.tlb /codebase

Microsoft (R) .NET Framework 程序集注册实用工具1.1.4322.573版权所有 (C) Microsoft Corporation 1998-2002。保留所有权利。
RegAsm 警告: 使用 /codebase 注册未签名的程序集可能会导致程序集妨碍在同一台计算机上可能安装的其他应用程序。/codebase 开关旨在仅用于已签名的程序集。请为您的程序集提供一个强名称并重新注册它。成功注册了类型程序集已被导出到“C:/Documents and Settings/pyw/My Documents/Visual Studio Projects/cscomtest/bin/Debug/cscomtest.tlb”，类型库注册成功
然后打开VB或者VBS，写KO！成功了，这个效果相当于用VB调用C#，虽然是通过COM实现的，太酷了！ 

set o = createobject("Test.MyTest")msgbox o.Fun()

 
```

# cvs 文件头

2007-06-08 12:58:00

```
在文件头加上如下这行即可


//$Id: log.h,v 1.2 2007/05/16 04:34:31 pengyuwei Exp $#


第一段是某种语言的注释符，VC就是//，Python是#，VB是'，诸如此类，后面按照这个格式写即可，在每次提交到CVS的时候，CVS会自动更新这一行的信息，方便吧。 
```

# 批处理一二三

2007-06-08 12:57:00

```
用net命令自动登录：
net use //1.2.3.4/share password /user:administrator
 
bat中跳转（冒号是在前面的，BT）：
:start...goto :start
 
bat中暂停：
首先建立一个vbs文件
Wscript.Sleep Wscript.Arguments(0) * 1000
然后bat中
start /w sleep.vbs 10 
```

# VS2003命令行编译

2007-06-08 12:56:00

```
前提是这些东西得在Path下:


path=%path%;"C:Program FilesMicrosoft Visual Studio .NET 2003Common7IDE"

编译命令举例如下：
devenv "W:productsrc est estg.sln" /rebuild "release" /out a.log


如果没有sln解决方案文件可以这样写：


devenv "Z:productsrc est estg.vcproj" /project "testg" /rebuild "release" /out a.log


 
VS2005的用法和2003一样，但是多了一个升级，对于2003的解决方案，可以先这样升级：


devenv "X:productsrc est estg.sln" /upgrade


然后再编译 
```

# [Python]编码问题

2007-06-08 12:54:00

```
m_result.append(objProj.m_name + ":编译成功")


UnicodeDecodeError: 'ascii' codec can't decode byte 0xb1 in position 1: ordinalnot in range(128) 如果objProj.m_name 的编码和字符串 ":编译成功" 的编码不同，就会有这个问题，解决方法是 objProj.m_name + u":编译成功" 加前缀u转换编码 改变默认编码的方法：

import sysreload(sys)sys.setdefaultencoding('utf-8')


 

做个试验：

>>> name="中文">>> print name + "编码"

中文编码
>>> name=u"中文">>> print name + "编码"

Traceback (most recent call last):  File "<interactive input>", line 1, in ?UnicodeDecodeError: 'utf8' codec can't decode byte 0xb1 in position 0: unexpected code byte print 只能打印正常的字符串,print 函数会尝试将unicode字符串转换为 ASCII，unicode字符串包含非 ASCII 字符，所以 Python 会引发UnicodeError异常 
```

# [NSIS]如何在结束页禁用取消按钮

2007-06-08 12:50:00

```
[NSIS]问题
看似简单，查了半天资料最后发现竟然得写一个回调函数实现，恐怖声明回调函数!define MUI_PAGE_CUSTOMFUNCTION_PRE "OnPreFinish"实现Function OnPreFinish  !insertmacro MUI_INSTALLOPTIONS_WRITE "ioSpecial.ini" "Settings" "CancelEnabled" "0"FunctionEnd 
```

# 苹果的方块光标

2006-05-23 09:58:00

```
怀念AppleII的方块光标，在VC其实也可以：
::CreateCaret(GetDlgItem(IDC_EDTINPUT)->GetSafeHwnd(),NULL,7,14);   ShowCaret(); 
但是不如苹果上的感觉好，不好用
```

# 最佩服中国农历

2005-02-24 13:00:00

```
正月十五雪打灯
好几天大晴天了，忽然昨天就飘起大雪花，下了整整一夜，入冬最大的一场估计也是最后一场雪
```

# 参加微软MDC大会

2004-06-26 11:36:00

```
昨天参加了微软首次在中国举行的MDC大会（移动开发者大会），总体感觉还是不错，尤其的是下午的专题讲座，还是学到一些东西的。不过有一个微软的专家讲POOM的时候竟然在Vs.Net的菜单里挨个找怎么把字体变大，最后也没有找到，然后把所有的代码复制到记事本中，又开始满记事本的菜单里找怎么放大字体，我坐在第一排，附近的人全都哗然，这样水平的人不知道怎么进的微软呀。唉，难怪微软被Sun超的一塌糊涂，现在dotnet出了这么久也不是Java的对手，从微软的这些‘专家’可知一二了。
```

# MSN小P机器人

2004-06-23 14:09:00

```
xiaop2005@hotmail.com joke看笑话 学习：L 问题 回答 还能查询公司的商品信息
```

