from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content.js').read_text(encoding='utf-8').split('=',1)[1].strip().rstrip(';'))
# Each row supplies a source page, a specific question, and four mutually exclusive answers.
# The first answer is correct; the application shuffles the answers before each session.
raw={
1:r'''6|Where does the course's PHP application run?|On the server|Inside the browser's HTML parser|Inside the CSS file|Inside the database table
7|What does the browser receive after the server processes a page request?|An HTTP response|The server's source directory|A Composer installation|A migration file
8|Which repeated job does a framework help organize?|URL routing|Replacing the operating system|Manufacturing the processor|Installing the browser for every visitor
9|Which arrangement separates responsibilities?|Separate data, request handling, and templates|Put all SQL inside templates|Copy setup into every page|Use a different database password for every HTML element
10|What does MVC name?|An application organization pattern|A database driver|A browser protocol|A file-upload encoding
12|Which file belongs in app/Models?|A data-access class|A public image|A CSS stylesheet|An HTML-only layout
13|Which task belongs to the View?|Display supplied task data|Choose database credentials|Install Composer packages|Define a migration
14|Which task belongs to the Controller?|Choose work for an incoming request|Store the MySQL service executable|Compile the browser|Replace all model classes
15|Which component receives model data before handing it to the view?|The controller|The browser's address bar|The CSS parser|The Apache control panel
16|Why does MVC help teamwork?|Developers can work on separate responsibilities|It removes every dependency|It prevents all programming errors|It eliminates the need for routes
17|Which language underlies CodeIgniter?|PHP|Java only|Python only|SQL only
20|Which tool manages the PHP packages in the setup?|Composer|Blade|Tinker|phpMyAdmin
20|Which local stack appears in the module?|XAMPP|Breeze|Eloquent|Intervention Image
21|Which command checks Composer's installation?|composer --version|php spark migrate|php artisan storage:link|npm run mail
22|What does create-project create in the example?|A starter project directory|One database row|A browser cookie|A CSS selector
23|Which alternative installation method does the module show?|Download the framework ZIP|Run a Blade directive|Create a session key|Use a resource route
24|Which folder holds logs and cache in the illustrated CI layout?|writable/|resources/views/|routes/|database/seeders/
24|Which folder contains Composer packages?|vendor/|app/Views/|public/uploads/|app/Controllers/
25|Where is Routes.php in CodeIgniter?|app/Config/|routes/|resources/|database/
26|Why keep app/ outside the public document root?|To prevent direct public access to internal source files|To disable all controller methods|To force SQL into HTML|To remove environment settings
26|What does URL rewriting direct requests through?|The front controller index.php|The task title column|The user password hash|The migration batch table
27|From which directory should php spark serve run?|The CodeIgniter project directory|Any browser download directory|The MySQL data directory only|The templates directory only
28|Which XAMPP service serves pages in the illustrated Apache workflow?|Apache|Breeze|Artisan|Eloquent
29|What does the default welcome page confirm?|The application starts and serves that page|Every database credential is valid|All task CRUD routes exist|Every upload is authorized
30|Which variable selects the CI environment?|CI_ENVIRONMENT|APP_DEBUG|MAIL_MAILER|DB_CONNECTION
31|Which ending does the module require for the base URL?|A trailing slash|A SQL semicolon|A file extension .blade.php|A question mark with no query
32|What does an empty indexPage setting affect?|The index.php segment in generated URLs|The database primary key|The name of the first user|The maximum upload size
33|In ?page=2, what is page=2?|The query string|A controller class|A model namespace|A view directory
34|Where are explicit CI route rules kept?|app/Config/Routes.php|resources/views/routes.php|database/seeders/Routes.php|public/Task.php
35|In Pages::about, what is about?|The controller method|The database driver|The route's HTTP verb|The Composer package
35|Which request matches a get() route?|GET|DELETE only|PATCH only|POST only
37|What does $1 refer to in the handler string?|The first captured route value|The first database row automatically|The first session cookie automatically|The first HTML heading
38|Which placeholder accepts one path component without a slash?|(:segment)|(:any)|(:database)|(:view)
38|Which placeholder can capture the remaining path across slashes?|(:any)|(:num)|(:alpha)|(:hash)
38|Which placeholder communicates a hashed-ID intent but matches like segment?|(:hash)|(:num)|(:alpha)|(:alphanum)
38|Which placeholder accepts alphabetic characters?|(:alpha)|(:num)|(:anyfile)|(:integeronly)
39|Which class does the sample controller extend?|BaseController|Mailable|Seeder|Migration
40|Which namespace appears in Pages.php?|App\Controllers|App\Mail|Database\Seeders|Illuminate\Models
42|Does an explicit Pages::about route run index() first?|No; it targets about()|Yes; always|Only after a database insert|Only after a file upload
44|Which clean-URL alternative does the PDF discourage for hosting?|Move the public entry files into the project root|Use the intended public document root|Keep credentials outside public access|Keep controller files in app/
46|Which extension do the CI view examples use?|.php|.blade.php only|.sql|.env
47|What does return view('about') do?|Render the about template|Redirect to the about URL|Insert an about record|Create the view file
50|Which PHP operator joins rendered view strings?|The dot operator|The SQL UNION keyword|The arrow operator alone|The array spread operator alone
51|What does view('directory-name/about') identify?|A view in a subdirectory|A database table with a slash|A remote website|A controller namespace''',
2:r'''6|Why replace fixed arrays with a database for task records?|To preserve and share records across requests|To eliminate all validation|To store CSS selectors as passwords|To avoid defining any schema
7|Which SQL command defines the tasks table?|CREATE TABLE|INSERT INTO|SELECT ONLY|SEND MAIL
7|What does AUTO_INCREMENT do for id?|Generates successive ID values|Hashes task titles|Encrypts every column|Creates Blade templates
7|What does PRIMARY KEY establish?|A unique row identifier|The default page title|A mail recipient|A public upload path
7|What does VARCHAR(150) describe?|A variable-length text column with a length limit|Exactly 150 rows|An upload limit of 150 KB|A 150-second session
7|What does NOT NULL disallow for title?|SQL NULL|Every duplicate string automatically|Every space character|Every lowercase letter
7|What is the default task status in the schema?|pending|done|deleted|authenticated
7|Which timestamp does the source schema define?|created_at|last_login_only|deleted_on_only|mail_sent_only
9|Which operation adds the demonstration rows?|INSERT INTO|CREATE TABLE alone|A route definition alone|A Blade loop alone
9|What does NOW() supply in the insert?|The current database date and time|The task's ID namespace|The upload MIME type|The controller name
9|How many demonstration tasks does the module insert?|Three|One|Five|Ten
9|Which demonstration task is marked done?|Fix login bug|Buy groceries|Submit report|All demonstration tasks
10|Which setting supplies the database server address?|database.default.hostname|app.baseURL|CI_ENVIRONMENT|MAIL_HOST
10|Which CI database driver appears in the setup?|MySQLi|Blade|SMTP|Breeze
10|Which setting supplies the database name?|database.default.database|database.default.DBDriver|database.default.username|app.indexPage
11|Where does CodeIgniter define database connection defaults?|app/Config/Database.php|app/Views/Database.php|public/Database.blade.php|routes/web.php
12|Which values override matching database defaults in the illustrated setup?|The .env values|The browser's heading text|The task-list HTML|The CSS file
13|Why keep real credentials out of committed config files?|To avoid exposing environment secrets|To make all database passwords blank|To remove the database driver|To disable SQL queries
14|Which page is useful for testing actual database access?|A page that runs a database query|Any static HTML page without a query|A CSS stylesheet|An unrelated browser bookmark
15|What does Unknown database usually indicate?|The named database does not exist|A missing view heading|An incorrect mail template|A missing CSRF label
15|What does Access denied suggest checking?|The database account and password|The Blade extension only|The upload dimensions only|The resource controller names only
15|What does Connection refused suggest checking first?|Whether the database service is running|Whether the task title is bold|Whether a mail component exists|Whether a CSS selector matches
18|What does the CI model extend?|CodeIgniter\Model|Illuminate\Mail\Mailable|App\Views|Database\MigrationOnly
19|Where is TaskModel.php stored?|app/Models/|routes/|resources/views/|public/uploads/
20|Which property selects the database table?|$table|$fillable|$baseURL|$indexPage
20|Which property identifies the key used by find($id)?|$primaryKey|$allowedFields|$hostname|$status
20|Does allowedFields create database columns?|No; the schema creates columns|Yes; on every page load|Only when Blade renders|Only when a session exists
21|What should replace manual SQL value concatenation in the illustrated queries?|Model and Query Builder methods|HTML interpolation inside SQL|A raw user-supplied column fragment|A CSS escape function
22|What is the purpose of new TaskModel()?|Create a model object|Insert a task immediately|Create a database immediately|Render tasks/index immediately
22|Which helper supplies the alternative model-construction style?|model()|asset()|route()|csrf_field()
23|What does find(3) use 3 as?|A primary-key value|A result-array position|A limit of three rows|A status length
23|What happens when find($id) has no matching row in the course example?|It returns null|It inserts the missing row|It always returns all rows|It renders a 404 view itself
24|Which condition selects pending tasks?|where('status', 'pending')|where('title', 'DESC')|orderBy('pending', 'status')|limit('status')
25|Which order places larger or later values first?|DESC|ASC|NULL|LIKE
25|Which order places smaller or earlier values first?|ASC|DESC|PRIMARY|UNIQUE
26|Which call retrieves the rows after the CI filter/order chain?|findAll()|view()|csrf_field()|password_verify()
27|Which method adds keyword matching?|like()|move()|destroy()|regenerate()
27|Which method limits the result count?|limit()|firstOrCreateOnly()|mime_in()|redirect()
27|Which method returns a count rather than fetched rows?|countAllResults()|findAll()|view()|getRandomName()
28|Which class must Tasks import to use the sample model name?|App\Models\TaskModel|App\Views\Task|App\Mail\TaskModel|Illuminate\Http\Task
29|Which view-data key produces $tasks in the view?|tasks|task_id|TaskModel|created_at
30|Which syntax reads the title from the course's CI array row?|$task['title']|$task::title()|Task.title|$task('title')
32|Which route pattern captures a numeric task ID?|/tasks/(:num)|/tasks/{task} in the CI example|/tasks?always=all|/tasks.blade.php
34|What must happen before reading fields from a possibly missing task?|Check whether the result is null|Print the field first|Insert a replacement automatically|Disable the model''',
3:r'''6|When must the controller validate submitted data?|Before saving it|After displaying success|After deleting the record|Only in the browser
7|Which route displays the CI new-task form?|GET /tasks/new|POST /tasks/new only|DELETE /tasks|PATCH /tasks/new only
7|Which route receives the create submission in the PDF?|POST /tasks|GET /tasks/new|GET /tasks/(:num)|DELETE /tasks/new
7|Which command lists CodeIgniter routes?|php spark routes|php artisan route:list|composer routes|npm run routes
8|Which form attribute identifies its destination?|action|name|type|value
8|Which form attribute selects POST or GET transport?|method|enctype alone|class|id
8|What determines the submitted text field's key?|Its name attribute|Its visible label alone|Its CSS class|Its placeholder alone
8|Which helper builds the application form destination?|site_url()|password_hash()|findAll()|getRandomName()
8|What does csrf_field() insert?|A hidden token field|A database password|A route parameter|A task record
9|Which call reads a posted title through the CI request object?|$this->request->getPost('title')|$model->find('title')|view('title')|session()->destroy('title')
10|What separates rules in the title validation string?|A pipe character|A slash only|A SQL comma only|A dot operator
10|Which rule limits the title to 150 characters?|max_length[150]|max_size[title,150]|limit[150]|maxlength:150
11|Which rule checks an email format?|valid_email|mime_in|uploaded|orderBy
11|What does is_unique[tasks.title] check?|Uniqueness in the named table column|The file's MIME type|The HTML attribute context|The session identifier
12|What does the validation failure branch return?|A redirect back with input|A successful insert|A delete response|A new schema
13|Which identifiers must agree for a field error to appear correctly?|The form name and validation/error field name|The CSS color and database port|The image width and user ID|The session timeout and route count
14|Which helper displays a CI field validation error?|validation_show_error()|wasChanged()|asset()|countAllResults()
14|What does old('title') recover after a failed form submission?|The previous submitted title|Every task title|The database password|The uploaded file bytes
17|Which CRUD operation changes an existing row?|Update|Create|Read|Seed
17|Which CRUD operation retrieves records?|Read|Create|Delete|Migrate
18|Which model call creates a task in the CI example?|insert([...])|Task::create([...]) as the CI call|view([...])|move([...])
18|Who sets the initial pending status in the create example?|The server's insert data|The browser's CSS file|The mail template|The file storage disk
19|Which model call changes one selected row?|update($id, $data)|findAll($data)|first($id, $data)|view($id, $data)
20|Why is a normal Delete link the wrong submission mechanism?|It makes a GET request for destructive work|It always makes a PATCH request|It validates every field automatically|It automatically checks ownership
21|What must the edit action load before rendering the form?|The existing selected record|A new random task|Every uploaded file|The SMTP connection
22|Which value has priority in old('title', $task['title'])?|Old submitted input when available|The saved value always|An empty string always|The newest task's title
23|Which variable identifies the target row in update($id, ...)?|$id|$rules|$uploadPath|$newName
25|Which encoding sends file bytes in the form?|multipart/form-data|text/css|application/sql|text/plain only
25|Which file-input name does the module use?|attachment|task_password|avatar_only|upload_status_only
26|Which file rule requires an uploaded file?|uploaded[attachment]|required_title|valid_email|orderBy
26|Which rule limits this CI file to 2048 KB?|max_size[attachment,2048]|max_length[2048]|limit(2048)|max_rows[2048]
26|Which rule allows the illustrated JPEG and PNG MIME types?|mime_in[attachment,image/jpeg,image/png]|is_unique[attachment]|numeric[attachment]|min_length[attachment]
27|Which method retrieves the uploaded file object?|getFile('attachment')|getPost('attachment') as the file API|find('attachment')|view('attachment')
27|Which method generates the stored upload name?|getRandomName()|getClientNameOnlyAsSafe()|password_verify()|old()
29|What does the third true argument in mkdir(..., 0775, true) request?|Recursive directory creation|Database transaction rollback|A 300-pixel crop|A public URL
30|Which CI image call creates the illustrated square display image?|fit(300, 300, 'center')|limit(300)|orderBy(300)|where('image', 300)
31|What must the model allow before writing attachment?|The attachment field|The SMTP password|The Blade directive|The route-list output
31|What does the database store in the public-upload example?|The generated filename|The entire uploaded file object|The image-service instance|The CSRF filter class
32|Which escaping context is shown for the image URL?|attr|sql|mail|route
32|What is the difference between a filesystem path and a URL?|One identifies server storage; the other identifies a browser resource|They are always identical strings|Both always start with FCPATH|Both always contain database credentials
34|Which operation comes before moving an accepted upload?|File validation|Printing success|Deleting the task|Sending the completion email
35|Which upload mistake does the checklist identify?|Storing privately but building an unrelated public URL|Using a random filename|Checking the file size|Saving only the filename
35|Does restoring old text input restore a browser's chosen file?|No; the user generally selects the file again|Yes; it restores local file bytes|Yes; it reconstructs every path|Only when the title is numeric
35|Does a writable-field list replace input validation?|No; they have different responsibilities|Yes; it validates all values|Yes; it checks every MIME type|Only when the table has an ID''',
4:r'''6|What problem does a session solve in the module?|Continuity across separate HTTP requests|Creating all database tables|Replacing route definitions|Resizing uploaded images
6|Which value is appropriate session data?|A logged-in user ID|A plaintext password|The entire users table|Every uploaded file's bytes
7|What does the browser usually keep to identify the session?|A session cookie|The server's complete session directory|The users table|The controller source file
8|Which call stores the demonstrated username?|session()->set('username', 'admin')|session()->find('username')|view()->set('username')|Task::createSession()
8|Which helper is a shorthand way to read username?|session('username')|view('username')|asset('username')|route('username')
9|Which operation removes one session key?|remove()|destroy() as the one-key operation|password_hash()|findAll()
9|Which operation ends the whole session?|destroy()|get()|first()|where()
10|Which value type suits a post-redirect confirmation?|Flash data|A permanent plaintext password|A new table schema|A route placeholder
10|When must flash data be set relative to the returned redirect?|Before returning the redirect|After returning the redirect|Only after the next page refresh|Only inside the database schema
11|Which call reads the flash message?|getFlashdata('message')|findOrFail('message')|store('message')|getRandomName('message')
11|What must match between flash-message storage and display?|The flash-data key|The database table size|The image dimensions|The SMTP port
12|What is the correct success-message sequence?|Save, set flash data, redirect, display|Redirect, save, display, set flash data|Display, redirect, validate, save|Delete session, create table, display
13|Why avoid storing large records in the session?|The session should hold only small necessary state|A session can store only one character|The browser cannot send HTTP requests|Models cannot read databases
14|Why is setting a message after return ineffective?|The return ends that method's execution path|The view automatically executes it later|The database always rejects it|The route changes to PATCH
15|Does reading flash data immediately delete it on that read?|No; its lifecycle is request-based|Yes; every read deletes it immediately|Only SQL reads delete it|Only template compilation deletes it
17|What does authentication establish?|Who the user is|Which image format was uploaded|Which migration ran last|The task list's CSS color
18|Which user column must contain a hash?|password|username|id|created_at
18|Why is username marked UNIQUE in the example?|To prevent duplicate usernames|To encrypt usernames|To turn usernames into images|To create the login route
19|What does password_hash() produce?|A stored password hash|The original password restored|A login route|An authorization policy
19|What does PASSWORD_DEFAULT select?|PHP's default password-hashing algorithm|The application's default username|The database name|The default session key
19|Is password hashing the same as reversible password encryption?|No|Yes; both decrypt with view()|Yes; both require the task ID|Only when the username is admin
20|Which model table does UserModel manage?|users|tasks|attachments|migrations
20|Why does the login example need a test user row?|The lookup needs a record with a stored hash|The view cannot render HTML otherwise|The framework requires exactly one account forever|Every route needs its own database
20|What is the printed demo username?|admin|root_user_task|student_portal_only|pending
21|What advantage does a filter provide over repeated manual checks?|A centralized reusable route gate|Automatic permission for every record|Automatic password recovery|Automatic database creation
22|What field type obscures typed password characters on screen?|password|hidden_title|email_only|numeric_only
22|Does a password input hash the password for storage?|No|Yes; automatically in the browser|Only on GET requests|Only with a CSS class
23|Which query retrieves the matched username row?|where('username', $username)->first()|findAll('password')|orderBy('username')->delete()|view('users')->first()
24|Which condition must be rejected before reading a missing user's password field?|No matching user record|A valid session key|A successful password verification|A rendered login view
24|Which function checks the typed password against the hash?|password_verify()|password_hash() as a direct string comparison|esc()|csrf_field()
24|Why not compare the typed password directly with the stored hash?|They are different representations|Hashes are always empty strings|PHP cannot compare strings|The username replaces the password
25|Which session flag does the course's filter check?|isLoggedIn|attachment|MAIL_HOST|tasks.index
25|Which session value identifies the authenticated row?|user_id|csrf_image_size|migration_batch_only|mail_port
25|Should the success session include the typed password?|No|Yes; always|Only for the admin|Only when the task is pending
26|Where does the logout method redirect after destroying the session?|/login|/tasks/create only|/storage|/database
26|Which method does the source's classroom logout route use?|GET|PATCH only|PUT only|CLI only
27|When does the authentication filter gate the protected controller?|Before controller work|Only after the response reaches the browser|Only during seeding|Only when a view changes
28|Which filter hook receives the controller's response afterward?|after()|before()|run()|rules()
29|Which type represents the incoming request argument in AuthFilter::before()?|RequestInterface|ResponseInterface|FilterInterface|TaskModel
30|Which alias entry points auth to the example filter class?|'auth' => \App\Filters\AuthFilter::class|'auth' => Task::class|'auth' => 'tasks.index'|'auth' => 'public/uploads'
31|Which route option attaches the alias in the example?|'filter' => 'auth'|'mail' => 'auth'|'view' => 'auth'|'table' => 'auth'
31|Does a login check establish record ownership automatically?|No; ownership needs an additional check|Yes; all logged-in users own every row|Only when the route is GET|Only when a flash message exists
33|What should a guest encounter when directly requesting a protected task page?|A redirect to login|Automatic administrator access|A task insert|A file download of the controller
35|Why is removing only username insufficient for logout?|Other login-state values can remain|It always deletes all tasks|It changes the database driver|It disables all routes''',
5:r'''6|Which existing knowledge transfers into Laravel?|MVC responsibilities|CodeIgniter file paths without changes|Spark command names without changes|CI placeholders without changes
7|Which command installs the illustrated Laravel installer?|composer global require laravel/installer|php spark install laravel|npm install codeigniter|php artisan create:composer
7|Which command creates the illustrated Laravel project?|laravel new myproject|php spark new myproject|php artisan storage:link myproject|composer migrate myproject
8|Which folder stores Laravel controllers?|app/Http/Controllers/|app/Controllers/ only|public/Controllers/|database/Controllers/
8|Which folder stores Laravel templates?|resources/views/|app/Views/ only|public/vendor/views/|routes/views/
8|Which file contains the course's web routes?|routes/web.php|app/Config/Routes.php|public/routes.sql|storage/routes.env
8|Which folder contains Composer-managed dependencies?|vendor/|routes/|resources/views/|public/uploads/
8|Which folder is the Laravel web entry point?|public/|database/|vendor/|storage/app/
9|Why does Laravel use predictable file locations?|To help tools and developers locate application parts|To remove all request handling|To store all secrets publicly|To prevent all user input
10|Which environment setting names the application?|APP_NAME|CI_ENVIRONMENT|MAIL_PORT|database.default.database
10|Which setting selects the illustrated local environment?|APP_ENV=local|CI_ENVIRONMENT=local_only|MAIL_MAILER=local|APP_URL=local
10|Which setting enables local debug output in the example?|APP_DEBUG=true|APP_NAME=true|DB_CONNECTION=true|MAIL_HOST=true
10|Which database connection does the foundation example select?|sqlite|MySQLi as its Laravel driver name|smtp|Blade
11|Does setting APP_URL start a development server?|No|Yes; automatically|Only when the title is set|Only when a task exists
11|What does a local virtual-host URL require besides APP_URL?|The corresponding local server/host setup|A mailable for that hostname|A task for each hostname character|A session named APP_URL
12|What reads environment values into Laravel configuration?|The config/ configuration files|The Blade task loop alone|The public image file|The browser's CSS parser
13|Which tool is Laravel's command-line interface?|Artisan|Spark|phpMyAdmin|Apache
13|Which address port does the simple Laravel server normally use in the module?|8000|8080 as the Laravel example|587|3306
13|Which command runs the project's fuller development script?|composer run dev|php spark routes|php artisan db:seed --class=DevServer|composer --database
14|What should you check when laravel is not recognized?|Composer's global bin directory on PATH|The task's status field|The upload's dimensions|The mail button URL
14|What does a port-in-use error indicate?|Another process uses that port|A missing Blade closing directive only|A duplicate username only|A missing image MIME type only
17|Must every simple Laravel route use a controller?|No; a route can respond directly|Yes; even a direct closure needs one|Only for CSS files|Only after logout
18|Which facade does the route example import?|Illuminate\Support\Facades\Route|CodeIgniter\Router|App\Models\RouteOnly|Database\Seeders\Route
19|What does the closure in Route::get execute for?|The matched request|Every database migration automatically|Every file upload on the machine|Every application on the server
20|Which CI file corresponds to Laravel's routes/web.php?|app/Config/Routes.php|app/Models/TaskModel.php|app/Views/about.php|writable/logs/
21|Which route helper directly renders a static view?|Route::view()|Task::viewAll()|Mail::view()|Storage::route()
22|Which key becomes $course in a view-data array?|'course'|'$course.php'|'resources'|'APP_NAME'
23|Which path syntax captures the ID in the Laravel example?|/tasks/{id}|/tasks/(:num) as its Laravel syntax|/tasks/$1 only|/tasks/<sql>
23|Does capturing {id} itself retrieve a database record?|No|Yes; always|Only when the ID is odd|Only when the view is about
24|After generation, where does PageController.php belong?|app/Http/Controllers/PageController.php|app/Mail/PageController.php|resources/views/PageController.php|database/seeders/PageController.php
25|Which namespace does PageController use?|App\Http\Controllers|App\Controllers as shown in CI|Database\Seeders|App\Mail
25|Which class does PageController extend in the Laravel example?|Controller|BaseController as its Laravel example|Mailable|Task
26|Which command lists available Artisan commands?|php artisan list|php spark routes|composer routes:list|npm artisan list
26|Which command lists Laravel routes?|php artisan route:list|php spark routes|php artisan mail:list-only|composer view:list
27|What does PageController::class identify in the route handler array?|The controller class|The Blade filename|The database connection|The task's title
27|What does the handler array's 'about' string identify?|The controller action|The .env file|The public directory|The primary-key column
28|What does view('about', $data) pass to the template?|Named values from the array|The database connection password automatically|All controller source files|All session values automatically
29|Which view filename matches Laravel's Blade example?|about.blade.php|about.sql|about.env|about.controller
30|Which response displays the supplied course and module values?|The rendered About page|The migration rollback log|The upload service object|The raw PHP source
31|Which value is still fixed in the first task-details demonstration?|The task title|The route's captured ID|The HTTP method name|The server's port configuration
32|Which syntax prints escaped Blade output?|{{ $title }}|{!! $title !!}|<raw>$title</raw>|SQL ESCAPE $title
32|Which Blade syntax permits raw unescaped output?|{!! $title !!}|{{ $title }}|@csrf|@method('PATCH')
33|Why does a missing controller import break a class-based route?|The route cannot resolve the intended class reference|The database deletes the controller|The browser rewrites it to SQL|The mail server changes the namespace
33|Which responsibility remains the controller's in both frameworks?|Coordinate the request and choose the response|Display every SQL column automatically|Store all images in the session|Replace the database schema''',
6:r'''6|Which component records table-structure changes?|Migrations|Blade templates|Mailables|CSRF tokens
6|Which component inserts repeatable sample records?|Seeders|The stylesheet|The route's HTTP verb|The public storage link
7|Where does SQLite store the database in the illustrated setup?|A database file|An SMTP inbox|A Blade component|A browser CSS rule
7|Which command runs pending migrations?|php artisan migrate|php artisan serve|php spark routes|npm run seed
8|Where are migration files stored?|database/migrations/|resources/views/|app/Mail/|public/uploads/
8|Where are Laravel model classes stored?|app/Models/|routes/Models/|resources/Models/|public/Models/
9|Why version a schema with migrations?|To reproduce database structure consistently|To store user passwords in source|To send an email per column|To bypass database configuration
10|Which schema call creates the illustrated tasks table?|Schema::create('tasks', ...)|Task::render('tasks')|Route::table('tasks')|Mail::create('tasks')
10|Which migration method creates a conventional ID column?|$table->id()|$table->view()|$table->csrf()|$table->route()
10|What does timestamps() add?|created_at and updated_at|Only task_status|Only user_password|A route and controller
11|What does nullable() permit for the notes column?|SQL NULL|Only an empty table|Only a numeric title|Automatic administrator access
11|What does default(false) provide for is_active?|A fallback false value on insertion|A permanent ban on updates|A generated password|A mail transport
12|What does migrate:rollback reverse?|The latest migration batch|The latest Blade render|The last browser click only|Every mail message
12|What does migrate:fresh do?|Drops tables and rebuilds the schema|Only adds missing sample rows|Only refreshes the browser|Only clears one session key
12|Where does the module permit destructive schema reset commands?|Disposable local development|A production database with real records|An email template|A read-only PDF viewer
13|Which command generates TaskSeeder?|php artisan make:seeder TaskSeeder|php artisan make:mail TaskSeeder|php spark migrate:TaskSeeder|composer seed:new
13|Which command runs only the named sample seeder?|php artisan db:seed --class=TaskSeeder|php artisan migrate --view=TaskSeeder|npm run TaskSeeder|php spark routes TaskSeeder
14|Where do the example seeder insert calls belong?|Inside run()|Inside the Blade head element|Inside the browser address bar|Inside the CSS selector
14|Which model does TaskSeeder import?|App\Models\Task|App\Mail\Task|Database\Views\Task|CodeIgniter\Task
14|Does rerunning a basic insert-only seeder guarantee no duplicates?|No|Yes; all seeders automatically synchronize|Only when the title is short|Only when no controller exists
17|What does one Eloquent model instance represent?|One record|Every database on the server|One CSS file|One migration batch always
18|What does generating the Task model NOT do by itself?|Insert the demonstration task records|Create a model class file|Place the file under app/Models|Give the class its Task name
19|Which property controls allowed mass-assignment attributes?|$fillable|$allowedFields as its Laravel property|$baseURL|$indexPage
19|Does fillable validate the content of title?|No; validation is separate|Yes; it applies all form rules|Yes; it checks MIME types|Only when the title is pending
19|Which default table convention pairs with Task?|tasks|TaskController|task_views|mail_tasks
20|Which earlier CI concept corresponds to Eloquent's model role?|CodeIgniter Models|CodeIgniter Views only|Spark's serve process|The Apache control panel
21|What does compact('tasks') construct?|An array using the existing $tasks variable|A new database table|A compressed upload file|A model query executed automatically
22|Which Blade variable receives the 'tasks' array key?|$tasks|$data_only|$TaskController|$created_at_only
23|Which directive begins the collection loop?|@foreach|@csrf|@method|@mail
23|How does the Eloquent task object expose title in the example?|$task->title|$task['title'] as its shown object syntax|Task/title|$task('title')
24|Which method executes the filtered Eloquent retrieval?|get()|view()|csrf_field()|move()
24|Which call filters the query to pending status?|Task::where('status', 'pending')|Task::orderBy('pending')|Task::findOrFail('pending')|Task::create('pending')
25|What response normally results when findOrFail cannot find the task?|404|Automatic insertion|A successful empty update|A new login session
25|What does findOrFail($id) search by in this example?|The primary key|The collection position|The status string's length|The upload index
26|Which method inserts an Eloquent record?|Task::create([...])|Task::all([...])|Task::findOrFail([...])|Task::latest([...])
27|Which action handles the task list route?|TaskController::index|TaskController::mail|TaskSeeder::run as the HTTP action|Task::rules as the HTTP action
28|Which stored value makes the view display Done?|done|pending|true_mail|complete_route
29|Which view displays the single task?|tasks.show|tasks.index_only|mail.tasks.completed|auth.login_only
30|What must exist before the demonstration list can show its sample tasks?|The migrated table and seeded rows|A mailable only|An attachment directory only|A session named title only
31|Which variable does the details view receive?|$task|$tasks_only|$migration|$smtp
32|Which command opens Laravel's interactive inspection shell?|php artisan tinker|php artisan serve|php spark routes|composer global list
32|What does Task::count() return in Tinker?|The number of matching task rows|Every task object|The first task title|The current mail port
32|What must you consider before first()->title on an empty table?|first() can return null|first() always inserts a row|first() returns the migration|first() starts Apache
33|Which layer should own the database query?|The model/controller data flow|The Blade display loop itself|The public image file|The browser's CSS parser''',
7:r'''6|Which method displays the create form in the illustrated workflow?|GET|DELETE|PATCH only|SMTP
7|Which command generates the Laravel controller for this module?|php artisan make:controller TaskController|php spark make:mail TaskController|npm create:task-controller|composer routes TaskController
8|Which name identifies the route that saves a new task?|tasks.store|tasks.create|tasks.edit|tasks.show
8|Is a route name necessarily the literal URL path?|No|Yes; always|Only when the title is blank|Only after seeding
9|Which forms in web routes need the illustrated CSRF token?|POST, PUT, PATCH, and DELETE forms|Only GET search forms|Only forms with a file|Only forms with two inputs
10|Which helper builds the named form action URL?|route()|asset() as the named-route helper|compact()|password_verify()
11|Which class supplies the injected HTTP request?|Illuminate\Http\Request|App\Models\RequestOnly|CodeIgniter\Model|Illuminate\Mail\Mailable
11|Does Request injection itself validate the form?|No|Yes; all fields automatically pass|Only for uploads|Only for task IDs
12|What happens after validation fails for the ordinary web form?|Redirect back with errors and old input|Insert the invalid record|Delete the current user|Return the mailable source
13|Which rule checks that the submitted title is a string?|string|required_image|mime_in|orderBy
13|What does max:100 limit for the title string?|Its character length|Its file size in KB|Its image width|Its number of database tables
14|Which variable contains the validation message inside @error?|$message|$task_id_only|$ruleset_name_only|$smtp_error_only
14|Which helper restores failed text input?|old()|latest()|store()|cover()
17|What happens first in the edit workflow?|Load the existing record|Save unvalidated edits|Delete the attachment|Send the completion email
18|Which route name identifies the update endpoint?|tasks.update|tasks.edit|tasks.create|tasks.index
18|Which HTTP method does the illustrated update route accept?|PATCH|GET only|SMTP|CLI only
18|Which parameter name pairs with Task $task for implicit binding?|{task}|{title_only}|(:num) in this Laravel example|{attachment_only}
19|What does implicit model binding supply?|The selected Task model instance|The complete task table schema|The current user's password|The Blade compiler object
19|Does binding alone prove ownership of the task?|No|Yes; every found row is owned|Only when the ID is numeric|Only when the upload is optional
20|Which CI concept matches Laravel's old() purpose?|Restore previous form input|Resize an image|Read SMTP settings|Create a migration batch
21|What does $task->update($validated) change?|The selected model's allowed attributes|Every user's records unconditionally|The Blade file itself|The route configuration file
21|Where does the shown update redirect?|tasks.index|mail.tasks.completed|database.migrate|storage.attachments
22|Why is the form's method POST while the route is PATCH?|A hidden method override supplies PATCH|Laravel ignores HTTP methods entirely|The form makes a GET request|The database selects the method
22|Which directive supplies that override?|@method('PATCH')|@csrf('PATCH')|@error('PATCH')|@foreach('PATCH')
22|Does the method override replace @csrf?|No|Yes|Only when the task exists|Only when the title is short
23|Which encoding does the upload form require?|multipart/form-data|text/sql|application/css|text/plain only
24|What does nullable mean for the illustrated attachment?|Absence/null is allowed; supplied files still need validation|Every file is accepted|The file must be empty|The field creates a SQL column automatically
24|Which rule restricts the attachment to image input?|image|integer|orderBy|required_title
24|What does mimes:jpg,jpeg,png restrict?|The accepted file types|The task statuses|The controller methods|The migration names
24|What does max:2048 measure for the file?|File size in KB|Image width only|String characters only|Task rows
25|Which check handles the optional file before storing it?|hasFile('attachment')|findOrFail('attachment')|wasChanged('attachment') as the upload-presence check|compact('attachment')
25|Which directory is passed to store() in the example?|attachments|tasks.index|app/Models|routes/web.php
25|Which disk is selected for the illustrated stored upload?|public|smtp|sqlite|blade
25|What does store() return for the task record?|The generated relative path|The complete uploaded object|The database password|The public disk object
26|What does storage:link expose in the standard local arrangement?|Public-disk files through public/storage|The .env file|Every private storage file automatically|Every controller source file
26|Which facade handles the illustrated old-file deletion?|Storage|Route|Schema|Mail
27|Which check prevents printing an attachment image for an empty path?|@if ($task->attachment)|@method('PATCH')|@csrf|@foreach ($task as $task)
28|When should a reliable replacement remove the old file?|After the replacement path is saved successfully|Before validating the replacement|Whenever the edit page opens|Before checking hasFile()
29|Which library supplies the shown Image facade?|Intervention Image|Eloquent|Breeze|Spark
29|What does cover(300, 300) prepare?|A square display image|A 300-row query|A session expiration|An SMTP connection
29|Which path helper supplies the illustrated absolute image-save path?|storage_path()|route()|old()|compact()
30|Which method holds the Form Request's validation definitions?|rules()|index()|content()|destroy()
30|How does a controller use the generated Form Request rules?|Inject the Form Request class for that action|Only generate the file and never reference it|Put the class name in CSS|Rename the upload to the class name
33|Does a database transaction automatically undo filesystem changes?|No|Yes; every stored file is rolled back automatically|Only for PNG files|Only with a named route''',
8:r'''6|How many CRUD operations does the acronym name?|Four|Seven|Three|Eight
7|Which option generates the resource method skeleton?|--resource|--markdown|--seed-only|--public-disk
7|What does --model=Task specify in the generation command?|The model associated with the controller|The mail sender|The upload disk|The task status
8|Does Route::resource implement validation and business logic automatically?|No|Yes; every action is completed|Only for uploads|Only when authentication exists
10|Which route name lists tasks?|tasks.index|tasks.create|tasks.store|tasks.destroy
10|Which URL displays the new-task form?|GET /tasks/create|POST /tasks/create|DELETE /tasks|PATCH /tasks
10|Which action handles POST /tasks?|store|create|show|edit
10|Which action handles GET /tasks/{task}?|show|store|destroy|update
10|Which action displays an existing-task form?|edit|update|store|destroy
10|Which action receives PUT/PATCH for a task?|update|edit|create|index
10|Which route name deletes a task?|tasks.destroy|tasks.deleteAll|tasks.edit|tasks.store
11|Which method normally applies newest-created ordering?|latest()|first()|create()|destroy()
11|Does Task::latest()->get() automatically scope to the authenticated user?|No|Yes; every Task query does|Only when a view is named tasks|Only when a task is done
12|Which action displays rather than saves the new-record form?|create|store|update|destroy
13|Which array should the normal store example pass to create()?|The intended validated fields|All raw request fields without checks|The entire session|The mail configuration
14|What do show and edit commonly receive through binding?|One Task model|The full migration collection|Every user record|An SMTP transport
17|What does auth middleware establish before the protected action?|The visitor is authenticated|The visitor owns every task|The task title is valid|The attachment has the correct MIME type
18|Which Composer option marks Breeze as a development dependency?|--dev|--model|--markdown|--name
18|Which Breeze installation flavor appears in the module?|blade|codeigniter|smtp|sqlite_only
18|Which command installs the scaffold's JavaScript dependencies?|npm install|php spark routes|php artisan tinker|composer db:seed
18|Which command runs the illustrated frontend development workflow?|npm run dev|php artisan migrate:fresh as the asset command|php spark serve as the Laravel asset command|Mail::send()
19|Which call groups protected routes under authentication?|Route::middleware('auth')->group(...)|Task::auth()->all()|Mail::middleware('auth')|Schema::authGroup()
19|Which route name identifies the protected dashboard example?|dashboard|tasks.dashboard_only|mail.dashboard|auth.tasks_only
20|Which earlier CI feature plays a similar route-gate role?|An authentication filter|An image crop|A seeder|A public filename
21|Which migration column associates a task with its owner?|user_id|attachment_size|smtp_port|route_name
21|Which relationship does User define for its tasks?|hasMany(Task::class)|belongsTo(Mailable::class)|hasOne(Route::class)|view('tasks')
21|Why create tasks through the authenticated user's relationship?|To associate the created task with that user|To bypass validation|To send email before saving|To expose every task publicly
22|Which query starts from the current user's task relationship?|$request->user()->tasks()|Task::all()|Task::latest() alone|User::all()
22|Which actions still need record-level access checks after a scoped index?|Show, edit, update, destroy, and uploads|No actions|Only the homepage|Only the migration command
25|Which setting selects SMTP transport?|MAIL_MAILER=smtp|APP_ENV=smtp|DB_CONNECTION=smtp|APP_URL=smtp
25|Which setting identifies the outgoing server hostname?|MAIL_HOST|APP_NAME|DB_DATABASE|MAIL_FROM_NAME
25|Which setting identifies the sender address?|MAIL_FROM_ADDRESS|MAIL_USERNAME always as the sender address|APP_ENV|DB_CONNECTION
25|Do placeholder SMTP settings send mail without a valid service?|No|Yes; any example hostname works|Only for completed tasks|Only with a resource controller
26|Where is TaskCompletedMail.php generated?|app/Mail/|app/Models/|routes/|public/storage/
26|Where is the Markdown email view generated?|resources/views/mail/tasks/completed.blade.php|app/Views/mail.php|database/mail.sql|routes/mail.php
27|Which optional command publishes mail views for customization?|php artisan vendor:publish --tag=laravel-mail|php artisan storage:link --mail|php spark publish:mail|npm mail:views
28|What does public Task $task in the constructor expose?|The received task as a public property|Every user's password|The SMTP secret as HTML|The route-list command
28|Does content() itself select the recipient and dispatch the mail?|No; it selects the content definition|Yes; it sends immediately|Only when Blade is disabled|Only for SQLite
29|Which Blade mail component supplies the message wrapper?|x-mail::message|x-task::database|x-route::csrf|x-storage::public
29|Which route does the email's View Task button target?|tasks.show|tasks.destroy|tasks.store|tasks.create
30|Which expression supplies the recipient in the shown send call?|$request->user()->email|MAIL_FROM_NAME|$task->title|APP_ENV
32|Which session message key carries Status updated after the redirect?|status|task_password|smtp_transport|migration_batch
33|Why combine wasChanged('status') with status === 'done'?|To target a saved transition to done|To send on every page view|To send before the update|To ignore whether the status changed
33|Does that condition guarantee exactly-once delivery under every retry?|No|Yes; it is a global delivery lock|Only when the title is short|Only when the route is GET'''
}
for n,text in raw.items():
    existing=[q for q in data['questions'] if q['module']==n and int(q['id'].split('q')[1])<=16]
    rows=[line.split('|') for line in text.splitlines() if line.strip()]
    assert len(rows)==44,(n,len(rows))
    for i,row in enumerate(rows,17):
        assert len(row)==6,(n,i,row)
        page,prompt,*choices=row
        assert len(set(choices))==4,(n,i)
        existing.append({'id':f'm{n}q{i}','module':n,'page':int(page),'topic':'Module review','prompt':prompt,'answer':choices[0],'choices':choices,'explanation':f'{choices[0]}. See Module {n}, PDF page {page}, for the source example and its context.'})
    data['questions']=[q for q in data['questions'] if q['module']!=n]+existing
data['questions'].sort(key=lambda q:(q['module'],int(q['id'].split('q')[1])))
(ROOT/'content.js').write_text('window.STUDY_DATA = '+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
print('Questions:',len(data['questions']),'; per module:',[sum(q['module']==n for q in data['questions']) for n in range(1,9)])
