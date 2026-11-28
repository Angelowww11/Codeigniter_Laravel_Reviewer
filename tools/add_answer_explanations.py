"""Attach authored, option-specific explanations without changing answer meaning."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
REASONS={}

# Each row gives the three incorrect choices in canonical order. The deployed
# explanation map uses choice text, so shuffling never changes its meaning.
REASONS[1]=r'''
1|Frameworks supply reusable mechanisms; the developer still writes the application's business rules.|Client-side checks can be bypassed. The server must still validate submitted data.|MVC separates data access from presentation instead of mixing both into each route.
2|The controller coordinates requests and responses; the model manages data responsibilities.|The view presents supplied data; it does not own persistence rules.|The router selects a handler from the request method and path.
3|The model handles data operations; it does not coordinate the complete request and response.|The view renders presentation after the controller supplies data.|A database driver communicates with a database; it does not coordinate MVC components.
4|This folder contains controller classes, not presentation templates.|This folder contains model classes for data operations.|This folder contains application configuration, including route settings.
5|The query and filtering requirements stay the same, so the model does not need the layout change.|The route selects the handler; it does not define the task-list layout.|Connection settings determine database access, not the arrangement of rendered records.
6|Serving the project root can expose internal source, configuration, or dependencies.|This contains internal application code and must not become the public file boundary.|This contains runtime files such as logs and sessions, not the public entry boundary.
7|This lists registered routes; it does not start the development server.|Artisan is Laravel's command tool, while this application uses CodeIgniter's Spark.|This creates a project from a package; it does not serve the existing project.
8|Duplicating SQL in templates mixes responsibilities and creates multiple copies to maintain.|Models handle data responsibilities; moving templates there reverses MVC separation.|A route should select the handler, not contain the shared database query and presentation.
9|The route target names a controller action; it does not identify a view variable.|The target does not select a model or model attribute.|The double-colon notation identifies a controller method, not a public filesystem path.
10|A route capture does not execute a model query.|A query-string value is separate from the captured path component.|The number identifies the capture position, not the number of URL components.
11|This can also match across slashes, exceeding the one-component requirement.|This is a numeric subset; it unnecessarily excludes nonnumeric segments.|This is an alphabetic subset; it unnecessarily excludes digits and punctuation.
12|Retrieval already succeeds. A package-manager version is not the next controller-to-view data check.|A favicon filename does not determine whether a view receives or loops over records.|The unrelated route does not explain the already-dispatched page's missing list output.
13|This obtains a model instance; it does not render a view template.|This creates a redirect response, asking the browser to request another location.|This accesses session services, not the view renderer.
14|The array value does not become the variable name; the key does.|The renderer exposes the supplied key as `$name`, not an automatic `$data` wrapper.|No `view` array with a `Pages` key is created by this data argument.
15|Template naming does not make a POST request match a GET route.|POST dispatch still depends on its registered route; it does not always select `index()`.|The public URL does not need a controller namespace to repair an HTTP-method mismatch.
16|Dot-separated nested view names are Laravel's convention, not this CodeIgniter identifier.|The identifier is relative to `app/Views` and omits the `.php` extension.|The file is a CodeIgniter PHP view, not a Blade template identifier.
17|Forwarding a route capture does not retrieve a database row.|The handler receives the captured value, not a count of path components.|`$1` is substituted with the first capture rather than passed as literal text.
18|A redirect produces another browser request instead of rendering this template in the current response.|A file's existence alone does not return its rendered content to the browser.|The base URL sets the application address; it does not render a template.
19|Models supply data, not the operation that joins rendered response strings.|Separate routes would create separate request handlers, not one combined response body.|A base URL is an address setting, not a list of view fragments.
20|A template heading cannot make the command shell find the project's `spark` file.|A table can affect a database operation, but the command fails before that stage.|A browser login cookie does not determine the shell's current directory.
21|The welcome page does not establish that database queries were executed successfully.|This request does not exercise every form or validation branch.|A public welcome page does not test server-side protection on private routes.
22|These are path components before the question mark.|This combines part of the path with the query separator and key.|GET is the request method, not the text after the question mark.
23|Moving SQL does not automatically change the route's HTTP method.|A change to one view does not remove data-layer responsibilities from every other page.|Putting a query in a view does not change the database's access permissions.
24|A primary-key setting changes record identification, not the application's generated address.|View files do not each need a namespace change to update the base address.|Dependency count does not select the URL used in generated links.
25|Authentication establishes identity; application rules still decide who may delete a particular task.|Composer installs packages. It does not automatically apply access rules to every route.|A visitor can bypass the page and make a direct request; permission must be checked on the server.
26|A static response does not require a database read.|A dummy model adds no necessary data operation to this page.|The model's data role does not require it to produce the contact-page HTML.
27|Templates are not the standard destination for CodeIgniter logs.|Composer dependencies belong in `vendor`; it is not the public upload or log directory.|Controller source files are not the runtime log destination.
28|Table and view counts do not determine whether this request matches its route.|Page titles do not control controller dispatch.|Package counts have no route-matching significance.
29|Rendering a view happens after dispatch; it cannot make a word match a numeric placeholder.|The pattern matches the path component, not a query-string `id`.|A route can capture an ID directly without storing it in a session.
30|This checks PHP's version, not Composer's installation.|This installs project dependencies; it is not the direct version check.|This creates a new project rather than simply reporting Composer's version.
31|This can capture slashes and therefore accepts more than the single slug component required.|This excludes nonnumeric slugs.|This excludes common slug characters such as hyphens and digits.
32|This stops at a slash, so it cannot capture the complete remainder as one value.|This cannot match the letters, slash, and extension in the remainder.|This cannot match the slash or the filename punctuation.
33|Controller inheritance does not define which filesystem files the server exposes.|A view-data key does not restrict direct requests for internal files.|The About route's method does not set the server's public directory boundary.
34|This contains application configuration, not Composer-installed package code.|This contains runtime writable data, not the dependency installation directory.|This contains public entry files and assets, not the Composer package library.
35|Controller classes belong here; the route configuration file does not.|This contains presentation templates.|The route definitions are application configuration outside the public directory.
36|Controller requests still enter through the public front controller and routing system.|Public assets remain available from `public`; only internal code stays outside it.|Filesystem placement does not create database tables or replace schema operations.
37|The front controller boots the framework; routing then selects a handler rather than directly exposing each template.|Migrations change database structure and are unrelated to the public HTTP entry point.|The web server runs server-side PHP; the browser does not provide the application's PHP interpreter.
38|An arbitrary PHP file does not make the project's `spark` entry file available.|The project-root `spark` file is not inside `public`.|The project command is not run from the dependency directory.
39|String concatenation affects response fragments, not Apache's incoming URL rewriting.|JSON responses are not a requirement for clean URLs.|A model is not required to configure the front controller's clean-URL path.
40|The welcome response need not execute a database connection or query.|A welcome request does not test all state-changing handlers.|Ownership checks require separate tests of the protected record actions.
41|This is Laravel's environment variable, not CodeIgniter's environment selector.|This sets the application address.|This controls the front-controller segment in generated URLs.
42|Routing names do not change the variables exposed by the view-data array.|Database storage is not needed to pass a local value to a template.|`index()` does not automatically create variables for another action's view.
43|Generated URL settings do not edit Apache or other web-server rewriting rules.|Routes still select their explicitly configured controller actions.|The URL front-controller segment has no effect on database primary keys.
44|The question mark separates this text from the path.|This is request URL data, not a response header.|A query string does not name a PHP controller namespace.
45|This is a controller path, not CodeIgniter's route configuration location.|This is Laravel's route-file convention.|Route configuration belongs outside the publicly served directory.
46|The action name after `::` is not a view-data key.|A namespace identifies a class location, not the selected action suffix here.|GET or POST is specified by route registration, not by the method name after `::`.
47|A POST request needs a matching POST-capable route.|PATCH does not match a GET-only route.|DELETE does not match a GET-only route.
48|The capture does not automatically query or select a database result.|The capture does not automatically read a session value.|`$1` is a substitution reference, not a query result limit.
49|This may match across slashes, beyond one component.|This also excludes nonnumeric components, which the general segment requirement does not exclude.|This also excludes digits and punctuation, which the general segment requirement does not exclude.
50|This cannot span the slash separating the remaining components.|This accepts numeric text, not an arbitrary remaining path.|This excludes slashes and nonalphabetic filename characters.
51|It has the same matching behavior, but does not express the question's hashed-ID naming intent.|This permits a broader remainder across slashes rather than the hash-intent alias.|A hashed identifier need not contain only decimal digits.
52|This permits more than alphabetic characters and does not state the alphabetic restriction.|This is broader still and can capture slashes.|This restricts the component to digits rather than letters.
53|This is not the CodeIgniter subdirectory identifier for the supplied PHP file.|This names a controller namespace, not a view path.|Views are resolved relative to `app/Views`, not as public PHP paths.
54|That namespace identifies model classes.|That namespace identifies configuration classes.|The application controller is in its `App` namespace, not the framework's namespace.
55|Explicit dispatch does not invoke `index()` as an automatic first action.|Controller actions do not automatically inherit the output of `index()`.|Returning a view does not change which action the explicit route selected.
56|This is the intended public boundary and keeps internal files outside direct access.|Keeping credentials outside public access reduces exposure.|Keeping controller source in the internal application directory is the intended separation.
57|The route targets `help()` directly; `index()` is not a required preliminary action.|Each action must deliberately supply its view data.|The absence of a model does not replace an explicitly selected action.
58|Rendering returns template content; it does not create a redirect response.|The renderer loads an existing template; it does not generate its source file.|Calling the view helper does not dispatch a controller action of the same name.
59|PHP uses `.` for string concatenation; `+` is an arithmetic operator.|`->` accesses object members rather than joining strings.|`??` selects a fallback for an unset or null value rather than joining fragments.
60|The view helper resolves a template path, not a controller class.|The identifier is relative to the view directory, not an absolute operating-system path.|A view identifier does not select a database table.
'''
REASONS[2]=r'''
1|Persistence does not validate request values; validation rules perform that separate check.|A local array is recreated with the request unless deliberately stored elsewhere.|The application server communicates with the database; the browser sends HTTP requests.
2|A Blade loop displays retrieved data; the connection fails before retrieval.|HTML escaping affects output, not whether the database accepts network connections.|A status condition is evaluated after a connection succeeds.
3|Matching environment values override the corresponding configuration defaults; the config file does not always ignore them.|Rendering a view does not select database connection settings.|Query-string values do not automatically override database configuration.
4|A normal environment file stores text; the editor does not automatically encrypt its secrets.|Credentials should not be exposed in a public URL.|An environment file configures the connection; it does not validate submitted records.
5|Changing MVC components does not create or select the missing database.|Sort direction affects rows after connecting to a valid database.|Writable-field settings do not repair the database name.
6|This is a controller base class, not the CodeIgniter data-model base.|This is Laravel's Eloquent base class, not CodeIgniter's.|This is an application controller base, not a database model.
7|This identifies the row key, not the table.|This selects permitted writable attributes.|This controls the form of returned records, not their source table.
8|This names the source table; it does not permit submitted attributes.|This names the row identifier.|This controls whether retrieved rows are arrays, objects, or entities.
9|This retrieves a specific primary-key row rather than the full set.|This retrieves the first matching row, not every row.|This returns a number rather than the row records.
10|The argument limits the number of results; it is not a primary-key lookup.|This retrieves up to three rows rather than the row identified by key 3.|This filters the status column rather than the primary key.
11|Filtering selects matching records; sorting requires an ordering operation.|The condition targets `status`, not the primary key.|`findAll()` retrieves records; a count needs a counting method.
12|Oldest-first order uses `ASC`, not `DESC`.|Ordering does not add a completed-status filter.|Ordering alone does not limit the result to one row.
13|This fetches matching rows rather than returning only their count.|This is a primary-key lookup, not a counting operation.|This returns the first matching row rather than a count.
14|An HTML heading cannot repair rejected database credentials.|A result limit applies after connection authentication.|Route order does not determine the database account's password or grants.
15|The singular `task` key does not create a plural `$tasks` variable.|The view path does not become an automatic `$show` variable.|The data key is extracted as `$task`; an automatic `$data` wrapper is not the contract.
16|A missing single-record lookup returns no record, not a collection of unrelated tasks.|A lookup does not create an unsaved replacement model.|The controller must decide how to turn a missing model result into a not-found response.
17|Title length is not the number of pending records.|Rendered HTML tags do not reliably represent database records.|Ordering does not filter pending status or execute a count.
18|Sorting changes order, not whether HTML tags execute.|Field permission controls persistence, not safe HTML output.|Changing connection credentials does not escape an already stored title.
19|HTML escaping does not create SQL parameter bindings.|Safe query construction does not make returned text safe for raw HTML output.|A route pattern constrains its matching path component, not every database input.
20|Table naming does not change the variable exposed by a view-data key.|Removing a primary key does not repair the controller-to-view variable name.|A count would replace the needed records with a number while leaving the naming error unresolved.
21|The request method does not change the returned row's PHP type.|Renaming a column does not make an array support object-property access.|Reading an existing row does not require inserting another row first.
22|A new row uses the defined default, not an implied completed state.|An applicable default is not overridden with NULL merely because the field is omitted.|Defaults are defined by the schema, not copied from the preceding row.
23|A repeated title cannot distinguish the two records.|Display positions can change with sorting, filtering, or deletion.|A formatted date is not guaranteed to be unique.
24|A view-data key does not choose the database connection.|A route placeholder describes the path capture, not environment configuration.|The form destination does not override the configured database automatically.
25|A NOT NULL constraint rejects SQL NULL.|If no valid default can satisfy the omitted required column, the constraint is not satisfied.|Explicit SQL NULL still violates NOT NULL.
26|The same static response still does not exercise the database.|A CSS request can succeed without any database connection.|Appearance changes do not test a data operation.
27|A PHP model setting permits attributes; it does not add the missing database column.|Naming a route does not alter the table schema.|Changing result order does not create a column.
28|Field protection restricts model writes; it does not remove database columns.|The route can receive POST data even if the model later excludes a field.|View syntax does not determine which submitted fields the model can save.
29|The row count cannot resolve a PHP class name.|Query ordering is not reached until the model class can be loaded.|HTML captions do not affect namespaces or imports.
30|Adding response HTML does not store shared records for future requests.|Renaming a request-local variable does not make its contents persistent.|Rendering twice still does not create persistent storage.
31|This requires an exact value rather than the intended contains-style match.|This changes result order rather than adding a keyword condition.|Counting without the condition cannot express the title search.
32|The logged correct data shows the retrieval path already succeeds.|Automatic key generation does not repair a template variable mismatch.|The model already obtained the correct record array; changing its table is not the direct correction.
33|Primary-key lookup is independent of the current display position.|The argument identifies one key rather than a row limit.|No title-length condition is specified.
34|Keeping secrets out of source control does not require an empty password.|The application still needs an appropriate database driver.|Secret management does not disable the application's data queries.
35|A response without a query does not test database access.|A static asset can load while the database is unavailable.|Listing routes does not execute their data operations.
36|Permission errors are normally reported as access-denied failures, not as a nonexistent database name.|Connection refusal means the service endpoint did not accept the connection.|An empty result happens after a successful database and query selection.
37|A database name alone does not check the configured account credentials and permitted access.|Sort order does not authenticate a database connection.|A Blade file is presentation code and cannot grant database access.
38|A missing row is a query result, not a refused network connection.|Writable attributes affect model writes after connecting.|Escaping protects output and cannot start a stopped database service.
39|A controller base does not provide the intended model API.|This is the Laravel ORM model base, not CodeIgniter's.|This is a controller class in the application namespace.
40|Controllers coordinate requests; this is not the model directory.|Views contain presentation templates.|Configuration files are separate from model class source.
41|This identifies the row key rather than the table.|This lists fields permitted for model writes.|This selects returned record type rather than the source table.
42|This names the table, not its lookup key.|This permits writable fields, not the identity column used for lookup.|This changes returned PHP representation, not which key is matched.
43|Permitting an attribute does not execute schema creation at startup.|Retrieving rows does not create columns from allowed-field names.|Rendering a view does not modify the database schema.
44|Displaying an unrelated first row hides the missing requested record and can show the wrong data.|A failed read should not silently create a replacement task.|Escaping the ID affects display, not whether the requested task exists.
45|Constructing the model object does not insert a row.|Schema creation needs a separate database setup or migration operation.|Construction alone does not call a row retrieval method.
46|This renders a template, not a model instance.|This creates a redirect response.|This accesses session services.
47|The argument is a key value rather than a display-order index.|A result count uses a limit operation, not this key argument.|The call does not specify the status column.
48|A view renderer does not execute the pending data retrieval.|The application's base address does not execute a model query.|The status column already supplies the filter; adding a duplicate column is unrelated.
49|Sorting by status does not exclude other statuses.|This compares the title rather than the status.|A limit restricts quantity without selecting the required status.
50|Ascending order places smaller or earlier values first.|Insertion order is not a substitute for the requested explicit ordering.|Without ordering, the query does not promise descending output.
51|Descending order places larger or later values first.|A column's data type does not itself request sorted output.|A query without ordering does not promise ascending output.
52|A primary-key lookup is not the explicit fetch-all operation shown for this filtered list.|This retrieves only the first matching record.|This returns a count rather than the matching row data.
53|This retrieves rows; it does not itself define a keyword condition.|This identifies records by primary key, not by a contains-style title match.|This retrieves one matching row without defining the keyword condition itself.
54|This retrieves rows and can accept a result bound, but `limit()` is the dedicated query-chain step being asked for.|This looks up a primary key rather than setting a general result limit.|This fetches one row rather than setting an arbitrary result-count limit.
55|This returns row data, not just the count.|This looks up records by primary key.|This returns a single matching record rather than a numeric count.
56|Ascending creation time gives oldest pending tasks first.|Sorting status neither filters pending rows nor orders by creation time.|This compares a date field with the word pending instead of filtering status.
57|The singular key exposes `$task`, not `$tasks`.|This key would expose `$TaskModel`, not instantiate or rename `$tasks`.|This key would expose `$items`, leaving `$tasks` undefined.
58|A count is a number and cannot supply five task records.|Title ordering does not identify the newest records or restrict the list to five.|Changing the model's identity column does not set a query limit.
59|This accepts nonnumeric path components too, so it does not enforce the stated numeric restriction.|This accepts alphabetic components rather than numeric IDs.|Query-string values are not captured as a path placeholder in that pattern.
60|Reading a field first can already raise the missing-result error.|An unrelated record is not a valid substitute for a missing requested ID.|A correctly shaped numeric ID can still identify no stored record.
'''
REASONS[3]=r'''
1|This starts the development server rather than listing routes.|This is Laravel's route-list command, not CodeIgniter's.|This lists Composer packages rather than application routes.
2|Another GET route still would not receive the form's POST request.|The failure concerns request dispatch, not record identity.|Storing HTML in a session does not register a receiving endpoint.
3|This supplies the token name rather than the complete hidden token field by itself.|This restores previous submitted input, not a CSRF field.|This displays a validation message, not the request token.
4|The `required` rule makes the field nonoptional, and the minimum length also applies.|The minimum and maximum define a range, not an exact three-character value.|`max_length[150]` explicitly supplies an upper bound.
5|This checks the ID column rather than duplicate task titles.|Length checking does not test uniqueness.|Presence checking does not compare the value with existing table rows.
6|Old input is the attempted submission, including values that were not saved.|Browsers do not restore the selected upload bytes through old text-input handling.|A redirect does not insert a new record or generate its ID.
7|This returns previous input, not the field's validation error.|This provides the error collection rather than the direct field-message helper requested.|This produces a CSRF input, not a title error message.
8|This changes an existing record rather than inserting the new row.|This removes a record.|This retrieves records without inserting one.
9|This creates another row rather than changing the selected one.|This retrieves the selected row without changing it.|The method expects the ID first and the update data second.
10|A maximum alone neither requires a value nor establishes the three-character minimum.|This requires at least 150 characters rather than the intended 3–150 range.|A uniqueness check on the ID does not define the title's required length range.
11|The saved title is the fallback only when no applicable old submitted value exists.|An error message describes a problem; it is not the user's attempted title.|The primary key identifies the record and is not either title value.
12|Ordinary URL-encoded form submission does not transport the file bytes in the required upload structure.|Plain text form encoding does not create the required multipart upload parts.|A plain JSON body is not the multipart file upload used by this form pattern.
13|This tests image content rather than expressing the required-upload condition.|This limits size; it is not the explicit presence rule.|This restricts accepted MIME types rather than expressing upload presence.
14|A current/original filename can retain client-provided collision-prone naming; it is not the random-name generator.|This returns the client-provided name rather than generating a new server name.|An extension is a suffix, not a complete collision-resistant filename.
15|An insert remains a create operation; later validation does not turn it into an update.|The controller's operation does not change the request method.|The browser can show errors, but that does not undo a row already written.
16|This persists rejected data and falsely reports success.|Removing a required rule hides the validation requirement rather than helping the user correct the input.|A silent list redirect loses both the attempted value and the explanation.
17|A renamed suffix does not establish the file's actual content or size.|The browser's file picker restriction is client-side and can be bypassed.|Keeping an original name provides neither type validation nor size validation.
18|The numeric size bound uses kilobytes, not an exact byte count.|Pixel dimensions require image-dimension checks, not a file-byte-size rule.|This validates one uploaded file's size, not the number of stored uploads.
19|Overwriting a shared filename can replace another visitor's file.|A task title is not a filesystem permission setting or a collision strategy.|Two rows pointing to the same path do not preserve two different files at that path.
20|Saving a filename string does not automatically store the uploaded bytes in the database.|A redirect does not repair a failed file move.|A filename alone cannot reconstruct the user's file contents.
21|This pattern stores a file reference, not an automatic binary copy in the column.|A visitor's local path is neither the server storage location nor a public URL.|Presentation markup does not identify the stored file using the intended data contract.
22|A server's absolute disk path is not generally a URL the browser can request.|A primary-key configuration identifies rows, not image resources.|A PHP namespace is not a browser-accessible image address.
23|A record ID does not resize or crop pixels.|Saving unchanged bytes does not establish square thumbnail dimensions.|Renaming a non-image file neither converts it to an image nor crops it.
24|A visitor can alter a hidden field before submitting.|Button text has no authority over the stored status.|The `required` attribute checks client-side presence, not the server-controlled initial status.
25|The first available row is not the requested target and may belong to another user.|An update request must not silently become a create request.|Dropping the ID can affect unrelated records instead of the intended task.
26|A title error does not create the filesystem destination.|Changing a read route does not make a directory writable.|A completed status does not prove the upload was stored.
27|Validation must occur before the write; redirecting afterward cannot validate retroactively.|The database insertion generates or assigns the ID, not the redirect.|The redirected GET still runs its receiving server handler.
28|Passing one rule does not override failure of another required rule.|The size check belongs before treating the upload as accepted.|Filename case does not reduce the file size or satisfy the failed rule.
29|Appearance settings do not determine route dispatch.|Seeded task titles are not evidence about the submitted request method and URL.|Password hashing does not register an upload endpoint.
30|Required presence is a separate rule.|Maximum length is a separate rule.|This uniqueness rule targets the named title column, not the primary-key type.
31|Writing an invalid row and reporting success contradicts the failed validation result.|The invalid submission has no legitimate saved task to return as a successful result.|Discarding all attempted input and errors prevents useful correction feedback.
32|A connection password is unrelated to mapping an error to an input name.|A template filename and displayed title do not identify the validated input field.|HTTP methods and CSS classes do not establish validation field keys.
33|This recovers a previous submitted value.|This creates a CSRF token field.|This generates an application URL.
34|Old input represents the submitted attempt rather than always using a schema default.|It does not retrieve the first task's title.|Validation rules describe constraints rather than the previously entered text.
35|Create inserts a new row.|Read retrieves existing records without changing them.|Delete removes a record rather than editing its values.
36|Create inserts records.|Update changes existing records.|Delete removes records rather than retrieving them.
37|The database title is only the fallback when old submitted input is unavailable.|The record identifier is not the attempted title.|A validation definition is not user input.
38|The title still needs its normal required, length, and uniqueness checks.|Editing should retain record identity rather than create a new ID to bypass validation.|A title's uniqueness requirement is unrelated to upload naming.
39|This creates a new row.|This reads the selected row without writing changes.|This removes the row instead of updating it.
40|GET does not automatically add a CSRF field or make destructive work safe.|A link does not automatically check ownership.|The label cannot turn an anchor's ordinary GET request into a protected POST or DELETE submission.
41|An empty object does not provide the selected record's saved values.|Fetching every task is unnecessary for a selected-record edit and moves selection into presentation.|Schema metadata does not supply the row's current field values.
42|The saved value is the fallback after old input is unavailable.|A route ID identifies the record and does not replace the title.|A validation error message should appear as feedback, not as the field's attempted value.
43|The data array supplies new field values; the ID identifies the selected target.|A heading does not identify the database row.|Row positions can change and are not the stable lookup key.
44|This ordinary encoding does not carry the required multipart file bytes.|Plain text is not the intended file upload encoding.|JSON alone does not create a standard multipart upload.
45|Another insert repeats the duplicate-row behavior.|A retrieval method does not persist the required update.|A button label cannot change the controller's database operation.
46|This is an image-content check rather than the explicit upload-presence rule.|This limits upload size rather than expressing required presence.|This restricts MIME types rather than explicitly requiring an uploaded file.
47|This sets a 2 KB bound, not 2048 KB.|A string-length rule is not the uploaded-file size rule.|Being an image does not establish the intended size limit.
48|A destructive GET can run when a visitor merely follows the URL.|Rendering a view should not delete records as a side effect.|Hiding a row changes appearance without deleting the database record.
49|A normal POST-field read does not return the uploaded-file object.|A query-string read does not return multipart file bytes.|A general scalar request-variable read is not the uploaded-file API.
50|This retrieves a filename rather than generating the intended random stored name.|This returns the original client-provided name.|An extension does not supply a complete generated filename.
51|Recursive creation concerns missing parent directories, not automatically publishing files.|Directory creation does not inspect uploaded content.|Creating a directory does not write a database file reference.
52|A valid CSRF token does not establish the correctness of every submitted value.|CSRF protection does not change the table schema.|A token does not automatically invoke all field or model validation rules.
53|An HTML label does not permit a model attribute to be persisted.|A route name does not add an allowed model field.|An original upload filename does not change the model's writable-field configuration.
54|GET is not the intended method for sending this file upload body.|Sorting records does not change form encoding.|A CSS class cannot add the missing multipart transport.
55|The database connection name is unrelated to the multipart input key.|A title POST value does not retrieve the uploaded file.|The destination folder name does not rename the field in the incoming request.
56|A server disk path and a public resource address have different meanings and need not be identical.|A URL does not automatically grant access to an arbitrary private server file.|Private filesystem locations are not necessarily exposed by the web server.
57|Saving a reference before acceptance can leave an invalid or missing attachment recorded.|A success response must not precede the checks that determine success.|Moving first does not remove the need to validate file content and size.
58|A generated filename is compatible with a correct public URL.|Size validation helps decide whether an upload is acceptable.|Saving a filename is valid when the server can reconstruct its correct public path.
59|Old-input storage does not repopulate a browser file input with uploaded bytes.|A redirect response does not make the browser upload the file again automatically.|An existing image reference does not restore a newly chosen browser file.
60|Permitted field names do not establish valid field values.|Field protection does not inspect a file's MIME content.|Field permission does not authorize the visitor to modify the selected record.
'''
REASONS[4]=r'''
1|Local PHP variables do not automatically persist or become shared across requests.|Passwords do not belong in request URLs; a session stores continuity data instead.|Remembering identity does not authorize access to every individual record.
2|This reads the value rather than storing it.|This removes the named value.|This reads a flash-data value rather than setting a normal session value.
3|This ends the session instead of removing only the requested value.|This reads rather than removes a value.|This writes a value rather than removing it.
4|Moving a template into the public directory does not create the login state the filter expects.|Printing a password in the URL neither establishes the intended session state nor protects the credential.|Task sorting does not control authentication continuity.
5|Complete permanent user records do not fit the short-lived-message purpose.|Flash data remains readable during its request lifetime; its first read does not immediately erase it.|A temporary message does not establish that a typed password matches a stored hash.
6|This checks whether a session key exists; it does not return the flash message itself.|This stores flash data rather than reading it.|This deletes the value instead of retrieving the message.
7|Later requests should not require the visitor's plaintext password in session state.|The stored hash is used for verification, not as a session login credential.|A session needs small identity values, not every account and its data.
8|This checks a password against an existing password hash.|This is a general hashing function, not the dedicated salted password-storage API requested.|This checks whether an existing hash needs an algorithm or options update; it does not create that hash.
9|Generating another salted hash does not verify the submitted password against the existing one.|A general hash comparison does not implement the stored password hash's algorithm and salt verification.|This checks hash-upgrade needs, not whether the submitted plaintext matches.
10|The username condition restricts the lookup to the supplied identity.|Finding a username is only the first step; the password still needs verification.|A read query does not insert a missing account.
11|Removing one value does not destroy the remaining session keys.|Browser history does not create a new account or establish valid server-side login state.|GET requests can read the current session just as other application requests can.
12|Checking only after a write is too late to prevent that protected action.|A rendered view is later than the required controller gate.|The gate must apply to protected requests, not only the initial login attempt.
13|This describes an HTTP request object, not the contract implemented by a filter class.|This describes an HTTP response object.|The authentication filter implements the filter contract, not a session-service interface.
14|This defines the filter class; its short alias must be mapped in the filter configuration.|Routes can apply filters, but the filter class definition does not belong in the route file.|A user model is not the filter-alias registry.
15|The filter checks existing identity state; login code must deliberately store that state.|Authentication is separate from validating submitted field values.|A basic login gate does not automatically implement per-record ownership rules.
16|A login flag identifies an authenticated session, not every role.|A username alone does not grant all application permissions.|Hidden controls can be bypassed by direct server requests.
17|An ordinary retained value does not automatically expire after the intended next-request lifecycle.|The password field is not message storage.|The base URL controls addresses, not temporary feedback messages.
18|A hidden link does not prevent a direct guest request to the write endpoint.|Title length validation does not authenticate a visitor.|Sorting records does not protect an unguarded update route.
19|The server can receive requests that did not originate from a displayed button.|CSRF protection does not establish a guest's login identity.|A model does not automatically know which page controls a visitor saw.
20|A database uniqueness rule does not connect a route alias with a filter class.|Upload encoding does not register an authentication filter.|Query ordering does not repair the missing filter alias.
21|An after hook runs after controller work and cannot serve as the first prevention check.|A footer renders after the protected action has already run.|A message display does not gate controller execution.
22|A successful login does not prove ownership of the requested record.|Authentication does not remove input-validation requirements.|Login alone does not grant permission to overwrite every attachment.
23|Local server memory is not automatically serialized into a browser cookie.|A redirect response does not transfer the controller's local variable state to the next action.|Model rows are stored data; they do not automatically become each visitor's authenticated session.
24|Destroying the whole session also removes authentication state, exceeding the narrow preference-removal goal.|Deleting an account is unrelated to clearing one temporary preference.|Removing the stored password hash damages future account verification rather than changing a preference.
25|Uniqueness identifies one candidate account but does not check its password.|A unique identity still needs record-level permission checks.|A database uniqueness constraint does not write session state.
26|Task attachments are unrelated to whether a matching account exists.|The filter checks access; it does not invent a user and password hash.|Submitting a username does not automatically register an account through session creation.
27|Button visibility does not prove the server rejects a direct protected request.|A public response can succeed whether or not protected access is closed.|Task count does not test the logged-out request path.
28|Renaming the field does not remove credentials from a GET URL.|A path parameter still exposes the password in the requested URL.|Flash data is not an appropriate substitute for the intended credential submission and verification flow.
29|The failure branch must not establish authentication state.|A success redirect contradicts a failed credential check.|A failed attempt must not replace the account's stored password hash.
30|Rendering a view does not reset the database.|The task model does not automatically destroy every browser cookie.|A redirect does not delete account records; the missing piece is saved authentication continuity.
31|A plaintext password is not needed to identify the authenticated database row.|The complete user collection includes unnecessary records and potentially sensitive attributes.|An SMTP credential configures mail transport, not the current visitor's identity.
32|Removing stored users breaks the successful-login precondition instead of testing it.|Removing the filter avoids testing its success behavior.|A bad upload tests validation, not whether an authenticated visitor can pass the same access gate.
33|A username is the readable login identifier, not the password-hash storage field.|The user ID identifies a row.|A creation timestamp records time, not a password verifier.
34|Redirects can use session-based flash messages when the value is stored before returning.|Flash messages do not need to be written into the task table.|An ordinary GET request does not automatically delete all session state.
35|A password hash is a one-way verifier, not reversible password encryption.|HTML escaping changes display representation and is not password hashing.|Hash generation does not verify credentials or create a logged-in session.
36|This PHP constant does not select a database encryption key.|It chooses an algorithm, not a shared user password.|The session ID is separate from password-hashing algorithm selection.
37|A password hash is verified without decrypting it back to the original password.|`password_verify()` returns a match result rather than recovered plaintext.|The database column type does not make a one-way password hash reversible.
38|This is the task-record table, not the account table in the stated model.|Attachment data does not provide the intended user-account rows.|Migration bookkeeping does not supply the application user records.
39|Hashing a message does not fix a mismatch between its written and read keys.|The request method does not rename the stored flash-data key.|A primary key identifies database rows, not session-message names.
40|A failed sign-in should not silently become account registration.|A read lookup does not require an insert first.|Creating a row is not proof that the submitted password matches an existing identity.
41|A reusable gate restricts protected actions instead of making them public.|A route gate uses authenticated state; the login process still verifies passwords.|Central authentication does not automatically define every record permission.
42|Text inputs show characters openly.|A hidden input is not a visible field in which the visitor types a masked password.|An email input validates a different kind of entry and does not mask it as a password field.
43|Password inputs mask display; they do not generate the server's stored password hash.|Obscuring characters is a presentation effect, not database encryption.|A CSRF field protects a different request property and does not hash passwords.
44|This treats the submitted username as a numeric primary-key value instead of comparing the username column.|This compares the password column with a username, which is the wrong lookup condition.|An unfiltered list does not identify the matching submitted username.
45|A uniqueness constraint helps identify one account and is not itself a reason to reject a valid result.|POST is the intended submission method in this login flow, not evidence that the user is absent.|A stored hash is the expected password representation for verification.
46|This creates a new hash rather than verifying against the stored one.|A general hash function does not carry out the stored password format's verification process.|This checks whether hash settings need updating, not whether the password matches.
47|A password hash and session identifier have different roles.|A password field normally sends the typed value; masking does not make that value empty.|Routing does not automatically rehash a username or verify a password.
48|This hashes the stored verifier itself instead of checking the submitted plaintext.|Direct string comparison compares different representations rather than performing password verification.|HTML escaping changes output representation, not password-match validation.
49|A username value is not the stored numeric primary-key value requested here.|A Boolean login flag does not identify which database row is authenticated.|A password should not be the session's row identifier.
50|Subsequent requests use authenticated session identity rather than retaining the typed password.|Avoiding further password entry does not justify storing the password in session state.|Masking the field does not protect a retained plaintext server-side copy.
51|A protected create-task page is not the guest sign-in form.|A storage path does not present the login action.|A database path is not the account sign-in endpoint.
52|The password field masks characters but does not create the storage hash.|Do not invent an application salt from an unrelated task title; use the password-hashing API.|A success message should not reveal the submitted password.
53|The protected controller must be gated before it can read or change protected data.|A completed response is too late to prevent the protected work.|Protected HTML should not be rendered before deciding whether the request is allowed.
54|The before hook acts on the request before the controller response exists.|`index()` is a controller-action convention, not the post-controller filter hook.|`login()` is an application action, not the filter response hook.
55|A response describes outgoing HTTP data, not the incoming request argument.|This is the contract implemented by the filter class, not the incoming request type.|A user model represents data access, not the HTTP request interface.
56|A missing lookup does not turn the username into a password.|No matching row can occur with a healthy database connection.|A missing identity should not trigger automatic registration in an existing-account login action.
57|Plaintext passwords are not an acceptable replacement for oversized session data.|Moving every user into a cookie still stores excessive and potentially sensitive account data.|Sessions are not file storage for all uploaded task content.
58|A signed-in visitor does not automatically own every database record.|Protecting an index does not authorize direct requests for every individual task.|Server-side rules determine ownership access; hidden links are presentation only.
59|Protected content should not be sent to a guest merely because navigation is hidden.|The access gate does not register an account automatically.|The redirect must precede the protected action, not occur after a successful unauthorized write.
60|Removing a username key does not restore a password.|A filter can inspect other keys, including a login flag or user ID.|Ending authenticated session state does not require deleting the account row.
'''
REASONS[5]=r'''
1|The frameworks use different router APIs; the CodeIgniter variable is not Laravel's route registration interface.|Blade presents content after routing; it is not the route-definition location.|An Eloquent query retrieves or changes data and does not replace request routing.
2|Migrations change database structure, not the rendered page layout.|Models handle data responsibilities; the question states that queries stay unchanged.|Seeders supply database records rather than page presentation.
3|This is CodeIgniter's route-file convention.|This is not the route location used by the taught current Laravel structure.|Views do not contain the normal web route registry.
4|This is CodeIgniter's usual controller directory rather than Laravel's.|This is not the standard application-controller directory.|The routes directory contains route definitions, not the controller class files.
5|This is CodeIgniter's view directory.|Public assets belong under `public`, but Blade source templates are not stored there by default.|This is not the standard Laravel Blade directory.
6|This names the application rather than its address.|This identifies the environment.|This controls detailed debugging behavior rather than the application URL.
7|This displays registered routes rather than starting the server.|This installs a global project-creation tool rather than serving the application.|Spark is CodeIgniter's command tool.
8|This creates an HTTP redirect rather than rendering a static view for the route.|This generates a URL for a named route; it does not register or execute the static-view response.|The view helper renders a template; that call is not the stated route registration API.
9|This untyped route closure receives the captured value, not an automatically resolved Eloquent instance.|The braces describe the path parameter before any query string.|The matched URL supplies the parameter; it is not an unrelated fixed view value.
10|This generates a model class, not the required controller.|Route inspection does not generate the controller source file.|This generates a view rather than a controller class.
11|This lists Artisan commands, not the registered route table.|This starts the server rather than showing route definitions.|This generates a controller; it does not inspect current route registrations.
12|The array dispatches to a controller method rather than naming a template and its data.|It does not configure a model's table.|The array entries are not the request URL and its query values.
13|Repeating a filename does not provide named template variables.|A namespace string identifies code location, not view data keys.|Template source is loaded from the view file; it is not the named-data argument.
14|Database and heading names do not make the missing action callable.|CSS and mail credentials do not determine controller method existence.|Seeding counts do not resolve a missing public controller action.
15|This deliberately allows raw HTML interpretation.|An ordinary PHP echo does not automatically escape the value.|A raw PHP echo does not apply Blade's normal escaped-output behavior.
16|The `course` data key does not create `$about`.|A request property is not created automatically from a value passed to the view.|The data value does not become a key inside an automatic `$view` wrapper.
17|The controller's local variable name is not automatically exported when the view-data key is `heading`.|No automatic `$data['title']` variable is created by that key.|The controller class name does not expose the supplied title value.
18|The view identifier omits the file extension and uses the template name beneath `resources/views`.|This mixes another directory convention into the Laravel view identifier.|The template is not resolved under the public asset directory.
19|Record titles do not repair an ignored route parameter.|The route registry is not a Blade presentation file.|A parameterized handler does not need one controller method for each possible ID.
20|A GET registration does not accept every HTTP method.|The existence of a form does not register its POST handler.|A single GET definition does not generate all resource actions.
21|Neither installing the creation tool nor creating the project is the same as starting its development server.|The installed tool still needs a project-creation command for each new application.|`laravel new` creates an application; it is not merely a migration runner.
22|Laravel permits numeric values in route parameters unless an incompatible constraint is configured.|The described fixed-ID behavior does not establish permanent Blade caching.|Different captured values can select different records through the same GET route.
23|This asks the browser to make another request instead of rendering during the current one.|A named-route helper returns an address, not the rendered view response.|This builds an asset address rather than rendering a Blade template.
24|A stylesheet is not the data-access layer.|Duplicating credentials in presentation does not restore separation.|Renaming a file does not move its database work into the correct component.
25|A text response does not exercise every template and its variables.|A template failure does not prove that the database has no records.|The successful route response is evidence that reinstallation is not the immediate template-level correction.
26|This supplies the application's address.|This selects the environment.|This controls debugging behavior rather than the displayed application name.
27|Blade interpolations should display supplied data, not each redefine connection settings.|An image directory does not configure the database connection.|Controller class names do not select environment database credentials.
28|The database name chooses a connection target, not the error-page detail setting.|A mail sender name does not enable application debugging.|Writable model attributes do not control detailed error pages.
29|Browser requests do not delete the project's command file.|The project contains `artisan` independently of database seeding.|Blade compiles view templates, not the project-root command entry file.
30|An environment value does not launch Apache.|Setting a URL does not run a shell command in the background.|Debug mode changes error detail; it does not turn a URL setting into a server launcher.
31|Changing a template extension does not configure local name resolution or the web server.|A display name is not a virtual-host or hostname mapping.|A model table setting does not create the local server address.
32|Blade delimiters display values; they are not the environment-to-configuration loading mechanism.|A captured URL value does not automatically configure the environment.|A seeder name does not populate application configuration settings.
33|Composer manages PHP packages and scripts; Artisan is Laravel's application CLI.|Spark is CodeIgniter's CLI.|Blade is Laravel's template engine, not its command-line interface.
34|A duplicate presentation class does not register the missing request path.|A schema migration does not connect the URL to a controller action.|A public image filename does not establish a route handler.
35|This executes database migrations rather than the Composer `dev` script.|This installs dependencies rather than explicitly executing that script.|This inspects routes instead of running the defined development script.
36|Route definitions cannot make a missing global shell command discoverable.|Mass-assignment settings do not affect the shell's PATH.|The browser URL does not select where the command shell finds executables.
37|An empty table is a data result, not a listening-port conflict.|Duplicate route naming does not occupy an operating-system TCP port.|A missing view variable does not prevent a server from binding its port.
38|Route closures can return valid responses.|`Route::view()` directly registers a static-view response without a separate controller action.|Direct route responses are not restricted only to plain strings.
39|A fixed text response does not require persistent storage.|A migration changes the database and is not the browser request's text handler.|Laravel supports direct responses without requiring a template every time.
40|The router runs the matched handler rather than every closure on every request.|Database migration execution does not invoke this HTTP route handler.|The route method and path determine dispatch, not a matching template filename.
41|This configures CodeIgniter application settings, not its explicit route definitions.|Controller class files are not the route registry.|Templates are not the route configuration file.
42|This registers a redirect rather than a view response.|This generates a named-route URL, not a static-view endpoint.|This generates an asset URL rather than registering a rendered view route.
43|Generating a class does not automatically register URLs for every method.|A database reset does not generate the page response and can remove stored data.|An environment file configures settings; it must not contain the controller source.
44|Raw output can interpret visitor-supplied tags rather than display them as text.|A database connection setting is unrelated to safe presentation of the name.|A route placeholder matches paths; it does not HTML-escape a displayed value.
45|Automatic model resolution requires the appropriate binding setup; a plain captured value alone is not a model.|Receiving an ID does not insert its database record.|Being numeric does not itself query the database.
46|This is CodeIgniter's controller-directory convention.|Route definition files are separate from the controller class directory.|Controller PHP classes do not belong in the presentation template directory.
47|This omits Laravel's `Http` namespace segment.|This is the application model namespace.|Application controllers belong to the `App` namespace, not this framework namespace.
48|These unrelated configuration values do not propagate the selected record ID.|Migration and package installation steps do not connect a request parameter to selected data.|A title, debug flag, and generated class do not establish the route-parameter data flow.
49|This lists registered routes rather than the available Artisan commands.|This starts the development server.|This lists Composer packages, not Artisan's command catalog.
50|This lists available commands rather than the route table.|This generates a controller instead of listing routes.|This reports migration state rather than HTTP route registrations.
51|A controller class reference does not name the Blade file.|A model chooses its table separately from the route's controller class.|GET or POST is supplied by route registration, not by the class reference.
52|The action can choose a view, but the handler string itself names the controller method.|The string is not the route's captured numeric value.|Database configuration is separate from selecting the action method.
53|The view receives the supplied named values, not every local controller variable automatically.|The template identifier does not replace the data values.|Rendering a view does not automatically retrieve or save a database record.
54|Internal source directories are not automatically served as public asset folders.|Static CSS files do not need to be stored as task records.|Blade templates do not use the migration directory as their asset source.
55|This is not the Laravel route-inspection command.|A Laravel project does not use a Spark entry point for routing commands.|This is not the standard command for inspecting Laravel routes.
56|A title-column default cannot resolve a PHP controller class name.|Seeded row count does not determine route class imports.|Image dimensions do not establish a controller namespace.
57|This is explicitly raw output.|A PHP echo inside a Blade PHP block does not automatically escape output.|A raw PHP echo does not add Blade's escaped-output behavior.
58|Double braces escape normal output rather than deliberately allowing raw HTML.|This explicitly escapes the value and then displays it through escaped output.|The leading `@` prevents server-side Blade evaluation of that brace expression.
59|Controllers need not move into the public directory to resolve their class name.|The missing PHP class reference is distinct from a database table lookup.|A Blade file should not duplicate the controller definition to repair an import.
60|Migrations are schema operations rather than the controller's general MVC role.|Models should not become the storage location for presentation HTML.|Querying directly in every view mixes data access with presentation instead of coordinating it through the controller.
'''
REASONS[6]=r'''
1|A seeder inserts records; it does not define schema changes.|A Blade view presents data rather than altering table structure.|Middleware checks or transforms requests; it does not define database columns.
2|This contains schema migration files rather than seeder classes.|This contains application models.|This is not the normal Laravel seeder directory.
3|That creates only the named timestamp column, not both conventional columns.|This adds a soft-delete timestamp, not the creation and update pair.|This adds the primary-key column rather than both timestamps.
4|A uniqueness constraint does not permit SQL NULL by itself.|A default value does not make the column nullable.|This adds timestamp columns rather than modifying nullability of the selected column.
5|This inserts seeder data rather than applying pending schema migrations.|This generates a migration file without executing its schema change.|This reports migration state rather than applying pending changes.
6|A normal rollback targets the last batch, not every migration and every backup.|Migrations track schema operations, not the most recently inserted task.|Seeding and migration batches are different operations.
7|That describes ordinary pending-migration execution, not a fresh rebuild.|That describes the default rollback scope rather than dropping tables and migrating.|A fresh rebuild does not restore deleted records from a backup.
8|The migration defines table columns; the seeder supplies row data.|A view or response renders the list, not the seeder.|Record authorization belongs in application access rules, not sample-data insertion.
9|This generates a controller class rather than an Eloquent model.|This creates a migration file instead of the model class.|This generates a seeder rather than the model.
10|This selects the table name rather than writable attributes.|This identifies the model's row key.|This converts attribute types; it is not the allowed mass-assignment list.
11|This returns one model or null rather than the complete collection.|This returns a number rather than task models.|This retrieves a specific primary-key row rather than all records.
12|`compact()` builds an array from variables; it does not execute a database query.|It reuses the existing variable value rather than retrieving a new collection.|Constructing view data does not rename the database table.
13|This retrieves only the first matching model, not the complete matching collection.|This executes an aggregate and returns a number, not the models.|This checks whether a match exists and returns a Boolean, not the model collection.
14|The method throws instead of returning a null model for Blade to handle.|It does not return an empty collection pretending to be a task.|A failed lookup does not create the requested record.
15|A collection is not one task; iterate it or select one model before reading its title.|PHP object-property access does not use a dot after the class name.|This attempts to call the model as a function rather than read its property.
16|This lists routes instead of opening the interactive environment.|This reports migration state.|This generates a model class and does not start an inspection shell.
17|An all-record collection does not perform a failing selected-ID lookup.|A query builder without retrieval has not resolved the requested record.|A count does not return the requested task or perform this not-found behavior.
18|Migrations describe schema, while Blade does not define that schema.|An Eloquent model's class is not the migration, and routes do not supply setup rows.|A namespace identifies code location, not the schema-and-seed responsibilities.
19|Text styling cannot create the missing table.|A theme does not execute a schema migration.|A descriptive seeder name does not prove that the table migration ran in the active database.
20|`all()` returns models in a collection, not the first title string.|An individual Eloquent model exposes its title to Blade.|The HTTP method does not turn a collection into one model.
21|This attempts a static-style method call rather than reading the model's title attribute.|A dot is not the PHP object-property operator.|This treats the model as a callable function.
22|Ordering by creation time does not add a completed-status condition.|The default latest ordering concerns creation timestamps rather than title alphabetization.|`get()` retrieves the matching collection without an automatic one-record limit.
23|A presentation loop is not a place to run migrations.|A fresh rebuild can remove data and should not precede checking the actual data and connection.|A route name does not determine whether the active database contains seeded rows.
24|This command changes database tables; it is not a Blade compilation command.|It does not merely change record order.|It affects the database schema and data rather than only browser session state.
25|The result is null, not a model with a particular empty title.|Tinker supports normal PHP object-property access when a model exists.|A missing result does not mean the title column was renamed.
26|A default value alone does not permit SQL NULL.|Uniqueness and nullability are different schema constraints.|Timestamp helpers do not make the notes column nullable.
27|Creating a row does not override the specified false default with true.|The column default is not automatically copied from the logged-in user's ID.|A default is defined by schema rather than the preceding row.
28|Controller naming does not determine the model's default table.|There is no standard `task_views` table convention for this model.|A seeder class name is not the inferred model table.
29|An array-construction helper does not require a database column named after it.|Changing the view identifier does not assign the missing `$tasks` variable.|Mass-assignment configuration does not create a local variable for `compact()`.
30|Unconditional insertion does not automatically remove old rows first.|Seeding does not automatically reverse migration batches.|Database rows do not turn into presentation templates after insertion.
31|A successful rollback does execute the migration's reverse operation; that is not the missing guarantee.|Successful rollback updates the migration bookkeeping, but does not promise restoration of lost row contents.|The supplied `down()` removes the schema change; the missing guarantee is recovery of the dropped data.
32|Title capitalization does not select the database file.|A heading attribute does not configure a connection.|Controller count does not choose which SQLite file receives migrations or queries.
33|A list cannot retrieve the intended rows from a table that has not been created.|Insertion needs the target table and columns to exist first.|Generating a controller after each insert is unrelated to setup ordering.
34|The Blade extension does not permit a mass-assigned attribute.|A displayed route label does not control Eloquent writable fields.|The observed field-permission issue is not explained solely by the database host name.
35|This mixes schema changes, presentation, and credential handling into unrelated layers.|Seeders supply setup data rather than render each visitor's list.|A migration is not the controller action for the visitor's GET request.
36|These commands rebuild schema state; they are not merely sample-row insertion commands.|A fresh rebuild drops tables and therefore does not preserve their existing contents.|Refresh replays migrations; it does not merely restart the HTTP server.
37|A display conditional does not validate a value during insertion.|The migration does not automatically normalize every unexpected runtime status.|A path placeholder does not validate a stored task status.
38|The generator does create the model-class source.|The generated model provides the place for model configuration.|The class can be used for queries once its database setup exists; generation alone does not insert demo rows.
39|This chooses the table name.|This identifies the model's primary key.|This controls attribute conversion rather than mass-assignment permission.
40|A permitted attribute can still contain an invalid value.|Required and length constraints need validation rules, not just a writable-field list.|A string column does not make `$fillable` validate the form value.
41|The standard table convention is plural for this model.|This is a class-style name, not the default table name.|A custom name is possible, but it is not required by the standard convention.
42|Views present supplied data rather than taking the equivalent model role.|Filters gate requests rather than providing the model's data API.|Environment files configure services; they are not the data-model component.
43|The helper does not query the database.|It constructs named data rather than selecting the template by itself.|It does not instantiate a new task model.
44|The singular variable would require a singular `task` key.|An `items` variable is not automatically created from the `tasks` key.|The renderer does not create that differently cased automatic wrapper.
45|This starts a conditional rather than iterating the collection.|This displays validation feedback rather than looping through records.|This checks whether a value is set rather than iterating it.
46|A writable-field list does not implement every business rule.|Migrations are setup operations, not a validation stage on every submission.|A database string type is not equivalent to the form's required and length checks.
47|This fetches one model rather than all matching models in a collection.|This returns a numeric count rather than the matched models.|This returns existence as a Boolean rather than a collection.
48|Ordering does not exclude tasks with other statuses.|Latest orders by creation time in the standard setup; it does not filter pending status.|Counting retrieves a number rather than describing the intended pending-record filter.
49|A missing lookup does not succeed by inserting the missing record.|The failure handler does not redirect to an arbitrary different task.|A missing record does not produce a guaranteed empty task object with the requested attributes.
50|A model query does not render a template through a `view()` method.|Renaming a seeder does not execute the pending query.|Debug configuration does not control how many task records are retrieved.
51|This reads all records rather than inserting one.|This performs a selected-record lookup rather than insertion.|This filters and fetches matching rows without creating a new record.
52|Mail is not the conventional list action in a resource controller.|A seeder's setup method is not the resource-list HTTP action.|A model rule method is not the conventional resource controller endpoint.
53|Strict comparison with `done` does not accept `pending`.|This is a different string and does not satisfy the condition.|This is another different string, not the stored value `done`.
54|This identifier points to a different template name.|This points into a mail-template namespace rather than the given tasks subdirectory.|This identifies a different authentication template rather than the supplied file.
55|`get()` returns a collection and does not guarantee that exactly one matching row exists.|A count requires a counting method rather than this retrieval.|The controller receives data; Blade must render it as HTML.
56|The key does not create that different plural variable.|A task view-data key does not expose migration state.|The supplied key does not create an SMTP configuration variable.
57|This starts the HTTP development server.|This lists registered routes.|This reports migration execution state.
58|A count returns a number instead of the task models.|A first-record lookup is a different operation.|A row count is not necessarily equal to the largest primary-key value, especially after deletions.
59|A first-record lookup does not insert an empty replacement.|Opening Tinker does not automatically run seeders.|Even a numeric route ID need not match an existing row, and this query has no guaranteed result.
60|The presentation loop should display records already supplied to it rather than own the database query.|A stylesheet is not application data-access code.|Migrations define schema changes and should not execute as the list's routine GET query.
'''
REASONS[7]=r'''
1|The existing create route displays the form through GET; it is not the receiving POST handler.|A migration filename is not a request endpoint.|A template's disk path is not the registered submission URL.
2|Title constraints are separate from the missing request token.|Table naming does not provide CSRF verification.|Sorting configuration does not protect the form submission from CSRF.
3|This supplies an HTTP-method override rather than the CSRF token field.|This displays validation feedback.|This is not the Blade directive that inserts the hidden CSRF field.
4|This represents the outgoing HTTP response rather than the incoming request.|This represents one uploaded file rather than the complete request.|This is the task data model, not the HTTP request object.
5|Failed validation must prevent the intended invalid write.|Failure interrupts the normal write path; it does not silently return an empty success result.|Validation failure does not call for deleting the selected record.
6|Required means nonoptional, and the maximum length still applies.|The rule is for a string title, not a file-size constraint.|The maximum is an upper bound, not an exact required length.
7|Old input presence does not identify whether the validator reported an error for that field.|The CSRF directive creates a request token, not field feedback.|Method spoofing does not display a title validation message.
8|Binding resolves the selected task rather than returning all users' tasks.|It resolves an existing model instead of always constructing an unsaved one.|The bound task is data; validation rules come from the request or validator.
9|CSRF verification does not change the request's effective HTTP method.|An error directive does not supply a method override.|Overriding to POST does not reach a route registered for PATCH.
10|The saved value is the fallback when previous submitted input is unavailable.|An error message is feedback rather than the attempted title.|The route ID identifies the task rather than the input value.
11|Image width requires a dimensions rule rather than this file-size bound.|The numeric file maximum does not limit filename character count.|This is an upper size limit in kilobytes, not an exact byte count or a presence rule.
12|The record needs a persistent file reference, not the temporary upload object.|Storage does not return presentation markup.|The browser's local path is not the server's stored relative path.
13|This starts the development server instead of creating the storage link.|This removes configured storage links rather than creating the public one.|Publishing package assets is not the normal public-storage-link operation.
14|Validation returns accepted values; it does not automatically persist a model.|It does not generate schema files.|Valid values do not establish ownership permission for a task.
15|This generates a controller rather than a Form Request class.|This generates a model rather than request-validation code.|This generates middleware rather than the intended Form Request.
16|A rejected upload should not cause the existing usable attachment to be deleted.|Merely opening an edit form does not request replacement.|If storage fails after deletion, the original file is already lost.
17|Failure must not persist rejected data or claim success.|An update still needs the intended target and validation checks.|Removing CSRF protection does not correct the invalid title.
18|A normal title error does not require the title to be a primary key.|Row count does not rename the validation field.|Laravel's error bag can display this message when the field name matches; a CI helper is not required.
19|The saved relative path already contains `attachments/`, so adding it again duplicates the directory.|The record ID does not replace the saved attachment path.|Internal model source paths are not the public storage URL.
20|Filesystem deletion is not automatically reversed by a later validation failure.|A filename string does not contain enough information to recreate deleted bytes.|A CSRF token does not back up file contents.
21|The saved title is the fallback, not the priority when old attempted input exists.|The numeric key is not the title the user tried to submit.|The update route name is an address identifier, not an input value.
22|Omitting an optional replacement does not request removal of the existing file.|An empty replacement file would destroy the usable attachment.|Another task's file is not a valid substitute for the unchanged attachment.
23|Passing validation rules does not override a failed authorization result.|The upload filename does not determine the Form Request's authorization decision.|A resolved Form Request runs its checks before the action proceeds.
24|A model does not make raw submitted fields acceptable or eliminate validation.|The attachment column should contain the intended file reference, not an arbitrary request object.|Visitors can modify hidden fields, so visibility is not a trust boundary.
25|Database row count does not resolve a PHP image-library class.|A valid route ID does not install or import the image-processing API.|A browser appearance setting does not determine package namespaces or method availability.
26|Returning a redirect first prevents the later checks and write from executing normally.|Old text input is not a backup of a deleted task or its files.|Success must not precede access checks, validation, and the intended write.
27|The database's larger capacity does not override the validator's stricter 100-character rule.|A writable-field list does not truncate text to a validation limit.|Blade does not convert a too-long string into a file upload.
28|Titles and mail subjects do not identify the filesystem location used for deletion.|A template name and image width do not select the stored file's disk.|Routes and migration batches do not make two storage disks equivalent.
29|A current request object does not prove permission for a selected record.|Injection does not automatically persist request values.|File processing still needs its own checks and storage operations.
30|Opening an edit page should not delete the current attachment.|The edit form needs the existing target before it can support a checked update.|Success cannot be established before finding the selected record.
31|The edit route presents the form; it is not the update-submission endpoint.|The store route creates a new task.|The show route presents the selected record without updating it.
32|A normal HTML GET form does not carry the intended POST-body method-spoofing workflow.|Standard HTML forms do not natively submit PATCH as their method.|A title field supplies neither CSRF protection nor the PATCH method override.
33|Implicit binding expects the route key to match the model parameter name in this pattern.|A `{user}` capture does not match the `Task $task` parameter.|A `{title}` capture does not match the model parameter name in the supplied implicit binding.
34|Finding a model does not authorize every user to change it.|The route identifies one task, not all task models.|Validation data comes from request validation, not route model binding.
35|Record existence and permission to modify it are separate checks.|A task can belong to a different user from the current visitor.|Presentation controls do not determine server-side ownership access.
36|Old-input restoration does not insert a record.|It does not inspect uploaded file content.|It does not resolve a model from a route parameter.
37|This instance operation targets the selected model rather than every task.|It changes permitted stored attributes, not only a model configuration string.|An instance update writes data rather than editing migration source.
38|Binding establishes the selected model, not the current visitor's ownership permission.|It does not return every task in the database.|The validated request array is a separate result of validation.
39|CSRF verification does not spoof the request method.|A route name does not change a submitted method.|Only the intended method-override input changes this POST form to an effective PATCH request.
40|This generates a CSRF token, not a method override.|This displays an error associated with a field named PATCH.|An override to POST would not select the PATCH handler.
41|Changing the effective method does not prove the request passes CSRF verification.|A task ID is not the CSRF token.|Existing-record forms still need the intended CSRF protection.
42|This encoding does not provide the expected multipart file upload.|Plain text is not the required multipart upload structure.|A plain JSON body does not create the multipart file parts used here.
43|Successful binding does show that a model was matched; that is not the missing permission check.|The supplied premise already establishes that a task model was resolved.|The supplied premise establishes record existence, but not ownership permission.
44|This permits a null value; it does not require nonnull uploads to be images.|This bounds file size rather than image content.|This is a database uniqueness rule rather than an image-content rule.
45|This rule checks content-derived file type; renaming a filename suffix alone is not sufficient.|File size requires its own maximum-size rule.|Pixel dimensions require a separate dimensions check.
46|Pixel width is an image dimension, not this file-size measure.|For this uploaded-file rule, the size unit is kilobytes, not title characters.|The rule does not count files already present in the directory.
47|A text-value read is not the uploaded-file presence API.|Old text input does not restore a new uploaded file object.|Generating a route URL does not inspect the current multipart request.
48|An optional nullable image field does not require a new file every time.|A missing optional replacement does not request deletion of the existing attachment.|The attachment's rules do not make the separate title field optional.
49|Pixels measure image dimensions rather than this file-size limit.|The original filename length is not the file-size unit.|The task-row count is unrelated to an uploaded file's size.
50|The method returns the storage reference; a browser URL must be generated for the chosen disk setup.|A visitor's local file path is not the stored server reference.|Storage does not automatically create or update an Eloquent model.
51|The standard public link does not publish every private disk.|It does not expose the whole application source tree.|The link exposes file resources, not a database column by itself.
52|A second text input does not change upload transport.|Database uniqueness does not add multipart file parts to the request.|Mail-server configuration does not control HTML form encoding.
53|An existing task ID does not prove that the task has an attachment path.|An upload validation error is not a test that a saved path exists.|The CSRF field does not decide whether to render an existing image.
54|Validation can fail, so deleting the existing file first risks losing the only usable attachment.|The replacement can fail during storage, leaving no usable old file.|Opening the form is not a successful replacement operation.
55|An UploadedFile object is temporary request data rather than the persistent path reference.|The visitor's local path is not the path assigned by the storage disk.|The model stores a file reference; presentation builds the image element later.
56|The arguments describe image dimensions, not a validation limit in kilobytes.|They do not define a filename length.|They do not create a filesystem disk configuration.
57|Validation-message count does not connect the public URL to the disk location.|A seeder namespace does not create the public storage link.|Sorting task statuses does not expose a stored image URL.
58|This decides whether the request is authorized, not its field constraints.|This returns the fields that passed validation; it does not define the rules.|This customizes validation messages instead of defining the constraints.
59|Running validation only after persistence is too late to prevent an invalid write.|A class name in the template filename does not apply a Form Request.|Generation alone does not connect the rules to the receiving action.
60|A database rollback does not restore files removed through the filesystem.|Committing database changes does not create missing file bytes.|Using a public disk does not add automatic filesystem rollback to database transactions.
'''
REASONS[8]=r'''
1|This registers the list endpoint only, not the full resource action map.|This renders one static view route rather than registering CRUD actions.|This registers the create-submission endpoint only.
2|Route registration does not implement the controller's validation and persistence logic.|A resource registration alone does not authorize access to each selected task.|An email workflow still needs its conditions, content, transport, and send operation.
3|The standard resource controller uses `destroy`, not a method named `delete`.|`remove` is not the conventional resource deletion action.|`update` handles the selected record's changes rather than its deletion.
4|Store receives the new-record submission rather than displaying the empty form.|Update changes an existing selected record.|Destroy removes a selected record instead of presenting a create form.
5|GET handles reading and form display, while POST handles resource creation; neither pair names the standard update methods.|POST creates and DELETE removes; these are not the update-method pair.|GET is not one of the standard resource update methods.
6|The create form is a GET form-display response, not a PATCH update.|A list action reads a collection; PATCH requests an existing record change.|Deletion uses the resource's DELETE action, not its PATCH update action.
7|This is the resource store request for a new record.|This invokes resource deletion rather than showing a record.|This opens the empty new-record form rather than showing the captured task.
8|An ordinary link makes a GET request and cannot become DELETE through its label.|The create endpoint displays the form rather than handling deletion.|This does not provide the intended POST-body DELETE override or CSRF-protected deletion workflow.
9|Authentication establishes identity, not ownership of every task.|Middleware authentication does not validate submitted field values.|Access middleware does not prove that an email transport will deliver a message.
10|That direction would describe the user belonging to one task, not the user's task collection.|That describes one related task rather than the intended many-task relationship.|Mailables are not the task records associated with the user's foreign key.
11|This orders the global task query without restricting ownership.|This reads all tasks without the user scope or the requested newest ordering.|This uses the correct user scope but orders oldest first.
12|A global query does not automatically log the visitor out.|Authentication middleware does not rewrite the owner of stored tasks.|Eloquent can query user-related tasks; the issue is that the supplied global query does not use that scope.
13|A visitor can submit another user's ID unless the server controls ownership.|A task title does not establish the authenticated owner.|The view is not authorized to select an arbitrary task owner.
14|The content definition does not itself choose the recipient or prove delivery.|A mailable's view selection is not a record-access decision.|Mail transport credentials belong in configuration rather than the content view definition.
15|This selects the recipient but does not perform the send operation.|Constructing the mailable alone does not dispatch it.|Rendering a view alone does not send an email message.
16|An unchanged done status fails the `wasChanged('status')` part.|A status transition is not an ownership authorization check.|This condition is evaluated for the saved status change, not title validation.
17|A task that was already done can satisfy this alone and cause repeated notices.|A title change is not a completion transition.|Opening a details GET page should not be the task-completion send trigger.
18|A scoped list does not constrain an independent global lookup in another action.|Title length does not decide permission to view another user's task.|Changing SMTP transport does not protect the show endpoint.
19|A valid title does not establish whether status transitioned to done.|Existing identity does not prove a workflow-state change.|List visibility does not determine whether the saved status changed in this update.
20|This reverses the parent-to-many-task direction.|Mailables are message definitions rather than user-owned task rows.|A route is not the user's one-to-many task relation.
21|Changing workflow status does not remove the task's owner.|A change back to pending can be a valid update.|`wasChanged` can be true, but the combined destination-state check still fails.
22|That is explicitly one of the true condition's checks.|That is explicitly what the saved-attribute-change check tests.|The conjunction does exclude an unchanged done status; it does not guarantee external delivery behavior.
23|Flashing feedback does not write the task's status attribute.|The flash key is not the mail server's authentication result.|The session message is not the controller's class or resource name.
24|Registering a second route does not encrypt or revoke the first registration.|A third group does not cancel unintended public endpoints.|Removing navigation does not prove the effective server route table is protected.
25|Login scaffolding does not implement every task operation and its application rules.|The remaining work includes data handling and access, not merely branding.|The mail sender is only one configuration detail and does not implement task behavior.
26|A mailable definition does not provision a mail-server account.|Task status is workflow data, not a transport credential.|Blade can render email content; the unresolved part is working transport configuration.
27|The risk concerns direct access to record-changing endpoints, not only presentation headings.|Changing route names does not supply the missing ownership checks.|An edit action's local access check is not automatically applied to every other action.
28|This applies oldest-created ordering rather than newest-created ordering.|This retrieves one model; it is not the general newest-ordering operation.|This retrieves results without adding newest ordering on its own.
29|Latest chooses ordering, not an ownership scope.|Authentication does not add a user condition to every global model query.|A task's workflow state does not create a current-user query scope.
30|Store persists a new submitted record rather than displaying the form.|Show displays an existing selected record, not the new-record form.|Update saves changes to an existing record.
31|This identifies the outgoing mail server rather than the displayed sender name.|This authenticates the transport account, not the sender's displayed label.|This is a database login setting rather than an email presentation setting.
32|The route-bound value represents one selected task, not a collection of every task.|Request validation returns a separate input array.|Binding does not generate migration files.
33|Authentication alone does not establish permission for an individual task.|Submitted fields still need validation.|Passing middleware does not guarantee that later database operations succeed.
34|This is a generator-related option, not Composer's development-dependency flag.|This does not mark a Composer requirement as development-only.|This does not classify the package in Composer's development dependency list.
35|The sender address and the explicitly selected recipient are different roles.|The task title is not an email sender address.|The SMTP hostname identifies a server rather than the selected recipient user.
36|Composer installs PHP dependencies rather than the JavaScript packages in this scaffold.|Migrations change database schema rather than installing frontend packages.|The scaffold installer prepares its frontend setup; `npm install` is the explicit JavaScript dependency installation command.
37|Selecting content does not authorize the record referenced by that content.|A view identifier does not configure the SMTP password.|Content rendering alone is not evidence of successful transport or inbox delivery.
38|A resource registration without middleware does not require login on its own.|A model condition is not an HTTP authentication route gate.|A route name prefix does not apply authentication middleware.
39|The server processes the destination request through its own access checks; email does not bypass them.|Generating a named URL does not authorize the future visitor.|A mail template does not remove private data to make every destination request safe.
40|A writable-field list controls model input attributes rather than route admission.|An old-input helper restores form values rather than authenticating requests.|A migration changes schema instead of guarding each HTTP request.
41|A task's own ID identifies that task, not automatically its owner.|Workflow status does not identify the user row.|A timestamp records creation time rather than ownership.
42|This is the opposite relationship direction from a user owning a task collection.|This limits the relation to one task rather than the intended many.|A mailable many-to-many relation does not represent the task owner association.
43|Associating ownership does not make title input valid.|A correct owner association does not grant universal task access.|Relationship creation is about record association, not sending before persistence.
44|A global task query lacks the current-user relationship scope.|Newest ordering alone does not restrict ownership.|A global user query does not start from the current user's task relation.
45|An index check only protects that list request.|Hiding edit controls does not protect the record endpoints.|Each independent selected-record action still needs the intended server-side permission check.
46|This sets a hostname string rather than choosing the transport driver.|A sender display name does not select the mailer.|The application environment name does not choose SMTP transport.
47|The port is a separate connection value, not the hostname.|This is the sender address, not the outgoing server.|This is the authentication username, which need not be the server hostname.
48|A server hostname is not the sender email address.|A numeric port is not an email address.|A transport username is for authentication and is separate from the configured sender address.
49|Nonempty values are not proof that an account or reachable server exists.|A Markdown view provides content, not an SMTP account.|A done task can trigger a send attempt but cannot make invalid transport credentials work.
50|This directory contains data models rather than mailable classes.|This directory contains HTTP controller classes.|This directory contains email view templates rather than the PHP mailable class.
51|This is the CodeIgniter view-directory style, not the Laravel Markdown view path.|A SQL file does not provide the generated Blade mail template.|A route file is not the mailable's content template.
52|The storage link command does not publish mail templates.|This is not Laravel's mail-view publication command.|This is not the supplied Artisan publication command for mail components.
53|A promoted constructor property does not itself send the message.|The received task property is not an SMTP password setting.|The typed parameter receives one task rather than fetching the whole collection.
54|Choosing the content does not dispatch the mailable to senders or recipients.|The Markdown view name does not select the authenticated recipient.|Task status does not make content selection perform the separate delivery operation.
55|This is not the provided Markdown message wrapper component.|The route/CSRF name is not the mail message wrapper.|A storage-disk name does not provide the Markdown email container.
56|Destroy is a state-changing deletion endpoint, not the task display link.|Store accepts a new-record submission.|Create displays the new-record form rather than the selected existing task.
57|Sending mail does not automatically reverse a failed model write.|The SMTP server does not validate the application's task update.|A mailable does not automatically persist the task it describes.
58|The flash-data key does not update the model's workflow-status column.|A local feedback message is not an SMTP delivery report.|It does not define validation constraints for a later update.
59|An already-done task with unchanged status fails the changed-attribute condition.|A workflow transition does not authorize access to every task.|The condition checks status, not merely title changes.
60|The condition inspects model-change state; it is not a durable global delivery lock.|Transport retries and application failures are not eliminated by the conditional.|Refreshing does not transform this local condition into an exactly-once delivery guarantee.
'''

CORRECT_ROWS={}
CORRECT_ROWS[1]=r'''
1|Frameworks provide reusable routing, validation, database access, and other infrastructure, reducing repeated implementation work.
2|The model owns data access and the application's data-related rules, keeping these separate from presentation.
3|The controller receives the routed request, coordinates data work, and chooses the response or view.
4|CodeIgniter resolves application PHP view templates beneath `app/Views`.
5|Only presentation changes here, so the view can change while the existing controller data and model query remain intact.
6|The document root should expose the public entry files and assets while keeping application internals outside direct access.
7|`spark` is CodeIgniter's project command entry point; its `serve` command starts the development server.
8|Shared query logic belongs in the data layer. Controllers can reuse it and supply different presentation templates.
9|`Pages` names the controller and `about` names the action method selected by the route target.
10|The route captures the numeric path value and substitutes it into `$1`, forwarding that value to the handler.
11|The segment placeholder accepts the required mixed characters in one path component while excluding slashes.
12|Retrieval already works. Check that the controller's view-data key matches the variable used by the template.
13|`view()` loads the named template, supplies its data, and returns the rendered content.
14|The array key `name` becomes the template variable `$name`; its value is the string `Pages`.
15|Dispatch depends on both HTTP method and path. A GET registration does not supply the missing POST handler.
16|CodeIgniter resolves this relative view path beneath `app/Views` and adds the PHP file extension.
17|The numeric path capture is 42, so `$1` forwards 42 to the selected profile action.
18|Returning `view('about')` places rendered template content in the current response rather than requesting another URL.
19|Rendered view fragments are strings. PHP's dot operator concatenates them into the intended response order.
20|The command refers to the project's `spark` file, so the working directory must contain that entry file.
21|The successful response proves that this page's request path works; unexercised database, form, and access paths remain untested.
22|The question mark separates the path from the query string, making `page=2` query data.
23|SQL in the template makes presentation responsible for data access, creating tighter coupling and duplicated logic.
24|The active base URL influences generated application links, so a stale value can keep producing the old address.
25|Framework tools do not know the application's deletion policy automatically. The developer must define and enforce the access rule.
26|A static template needs no database operation. The controller can return the view directly through its route.
27|CodeIgniter stores runtime output such as logs in `writable`; the destination must also allow the required server writes.
28|Compare the incoming method and path with the registered pattern and handler before investigating unrelated page details.
29|The numeric placeholder rejects a word such as `alex` because that path component does not satisfy its numeric pattern.
30|`composer --version` directly checks that the shell can run Composer and reports its installed version.
31|A segment fits one slug component and accepts characters such as hyphens without allowing the capture to cross a slash.
32|The any placeholder can capture a remaining path containing slashes, matching the intentional multi-component remainder here.
33|The server's document root controls which filesystem paths are directly exposed, independently of normal controller routing.
34|Composer installs the project's PHP package dependencies into `vendor`.
35|Explicit CodeIgniter routes are application configuration stored in `app/Config/Routes.php`.
36|Requests can still reach controllers through the front controller while their source files remain outside the public boundary.
37|Rewriting sends the request through `index.php`, where the framework boots and dispatches its routes.
38|The project-root directory contains the `spark` command file used by `php spark serve`.
39|Removing `index.php` from generated links does not configure Apache. Incoming clean URLs still need working rewrite handling.
40|The welcome page tests application startup and its own response, not every database or security feature.
41|`CI_ENVIRONMENT` selects CodeIgniter's operating environment, such as development or production.
42|The renderer uses the data-array key `displayName`, so the view receives `$displayName` rather than the controller's local name automatically.
43|The setting controls the front-controller segment used in generated URLs. Incoming URL rewriting is a separate server requirement.
44|Text after `?` supplies query-string parameters rather than another component in the route's path.
45|`app/Config/Routes.php` contains the explicit method, path, and handler definitions for CodeIgniter.
46|The part after `::` selects the public controller action method.
47|The route's GET registration matches a GET request rather than the listed state-changing methods.
48|`$1` is a back-reference to the first captured route value and is substituted into the handler target.
49|A general segment accepts the specified mixed single component without spanning a slash.
50|The any placeholder can span slashes when the handler intentionally accepts the remaining path.
51|The hash placeholder communicates hashed-ID intent while using the same matching behavior as segment; it does not verify a cryptographic hash.
52|The alpha placeholder enforces an alphabetic capture rather than accepting arbitrary segment text.
53|`account/profile` resolves the PHP template relative to `app/Views`, without including its extension.
54|A controller in this application directory belongs to the `App\Controllers` namespace.
55|The explicit route calls `about()` directly. `index()` is not a mandatory prelude to every controller action.
56|Moving entry files without preserving the public boundary can make internal project files directly reachable from the web server.
57|The explicit route selects `help()`; it does not execute another action first merely because that action is named `index`.
58|The helper renders the existing About template and returns its content for the response.
59|PHP uses the dot operator to concatenate rendered strings such as header, main view, and footer.
60|The slash selects a view subdirectory relative to CodeIgniter's configured view location.
'''
CORRECT_ROWS[2]=r'''
1|A database persists shared task records beyond the lifetime of a controller action or server process.
2|Connection refusal occurs before query execution. First check that the database service listens at the configured host and port.
3|Matching active environment settings override the corresponding connection configuration defaults.
4|An uncommitted environment file separates deployment-specific credentials from code shared through source control.
5|The server is reporting a database-name problem, so compare the configured name with the databases actually available.
6|Extending `CodeIgniter\Model` supplies the model API and configuration used by the CodeIgniter task data layer.
7|`$table` names the table that supplies this model's records.
8|`$allowedFields` restricts which submitted attributes normal protected model writes can persist; value validation remains separate.
9|`findAll()` retrieves the model's row collection rather than a single primary-key result or a count.
10|`find(3)` uses 3 as the primary-key value to identify the requested record.
11|The where condition selects pending rows, and `findAll()` executes retrieval of those matching rows.
12|Descending creation-time ordering places later timestamps before earlier ones.
13|`countAllResults()` returns the number of rows matching the query instead of fetching their full row data.
14|Access denied concerns connection authentication or privileges, so inspect the account, password, and allowed database access.
15|The `task` data key exposes `$task` in the selected template.
16|A missing single-record `find($id)` lookup returns null; the controller must handle the absence before reading fields.
17|The badge needs an aggregate number. Apply the pending condition, then count the matching records.
18|HTML output escaping displays the stored title as text instead of allowing its tags to execute in the page.
19|HTML output and SQL query construction use different interpretation contexts. Protection for one does not automatically protect the other.
20|The view variable comes from the supplied data key. Align `items` with the variable used in the loop.
21|An array row needs array-key access such as `$task['title']`; object-member syntax requires a matching object return type.
22|When the insert omits this column, its applicable schema default supplies the initial pending value.
23|A unique primary key identifies one record even when titles repeat or display order changes.
24|The matching active environment settings take precedence, so stale values there can select another database despite the config defaults.
25|An empty string is a nonnull value. Required-text validation needs more than a NOT NULL constraint.
26|Only an executed data operation exercises the application's configured database connection.
27|Writable-field permission does not define table structure. The database still needs a compatible column.
28|The model's field protection can exclude a submitted attribute even when the form and database column both exist.
29|PHP must resolve the model class through its namespace and import before any query can run.
30|Database storage survives individual requests; the model retrieves those persistent records when each new action needs them.
31|A title `like` condition expresses keyword matching rather than exact equality or result ordering.
32|The logged array establishes that retrieval succeeded; the mismatch is in how that data reaches or is read by the view.
33|The value 8 is matched against the configured primary key, independently of the row's displayed position.
34|Committed credentials can expose environment secrets to everyone with repository access.
35|A page that actually executes a query tests the database path rather than only static response handling.
36|The named database cannot be found under the requested connection, unlike a successful query returning no matching rows.
37|Check the credentials and account access when the server rejects database authentication.
38|A stopped or unreachable database endpoint can refuse the connection before any table query or view rendering occurs.
39|The CodeIgniter model base supplies the expected configuration and record operations.
40|Application model classes are stored under `app/Models`.
41|The table property selects the source table; it does not select field permissions, row identity, or return representation.
42|The primary-key property identifies which column the model uses for keyed record lookup.
43|Allowed fields are a write-permission list. Table columns must exist through a separate schema definition or change.
44|A nonexistent ID supplies no row. Return an appropriate not-found response before trying to read the task's title.
45|The constructor creates a PHP model object; insertion, retrieval, and schema work are separate operations.
46|The `model()` helper supplies CodeIgniter's alternative model-instantiation style.
47|The find argument identifies a primary-key value, not a row offset, result limit, or status condition.
48|A filter describes the query. A terminal retrieval operation is needed to fetch its matching rows for the controller.
49|The where condition explicitly compares the status column with pending.
50|Descending order puts larger values or later timestamps before smaller or earlier values.
51|Ascending order puts smaller values or earlier timestamps first.
52|`findAll()` explicitly executes the filtered model retrieval and supplies its matching rows.
53|`like()` adds the keyword condition; retrieval methods execute a query but do not themselves define that search condition.
54|The dedicated `limit()` builder step adds the maximum result count before retrieval.
55|The count method supplies a number, which differs from either a row collection or a single-record lookup.
56|The chain filters pending status, orders creation time newest first, and then retrieves the matching records.
57|The plural `tasks` key becomes the plural `$tasks` variable inside the view.
58|Descending creation time chooses the recent records, and a limit bounds the displayed collection to five.
59|The numeric placeholder captures an ID-shaped path value; record existence still needs a later lookup.
60|Null means there is no task row. Check that result before accessing any record field.
'''

CORRECT_ROWS[3]=r'''
1|Spark's routes command lists registered methods, paths, and handlers, helping compare the form request with actual dispatch rules.
2|Displaying the form and receiving its submission are separate routes. The POST needs a matching receiving handler.
3|`csrf_field()` generates the hidden field carrying the token expected by the enabled CSRF protection.
4|Required rejects an absent or empty value; the two length rules establish the inclusive 3–150 character range.
5|The unique rule names the tasks table and title column to check for an existing matching title.
6|`withInput()` keeps the failed form values available to old-input helpers on the redirected form request.
7|The helper selects the error associated with the title field so the message can appear beside that input.
8|`insert()` performs creation of a new row from the intended data.
9|The ID identifies the existing target, and the data array supplies the field changes to apply to that row.
10|The requirement needs presence, a three-character minimum, and a 150-character maximum; all three constraints must be expressed.
11|Old submitted input has priority after failure; the stored title supplies the fallback for the initial edit display.
12|Multipart form encoding carries the uploaded file bytes as a file part rather than only ordinary text fields.
13|The uploaded rule explicitly requires a file for that named upload field; type and size rules serve different checks.
14|A generated random name avoids relying on a visitor-controlled original name and reduces accidental collisions.
15|Validation after insertion is too late to prevent an invalid row from being written. Reject invalid input before the write.
16|Old input preserves the user's attempted values, and field errors explain what must change before resubmission.
17|The server must check actual upload properties. A renamed extension or browser picker restriction is not sufficient evidence.
18|The numeric argument in this uploaded-file size rule is the maximum size in kilobytes.
19|Different accepted uploads should receive separate server-side filenames rather than compete for the same storage path.
20|A saved filename is useful only when the corresponding file was stored successfully; failed movement must not produce success feedback.
21|This pattern stores a generated filename reference; the view can combine it with the configured public upload URL.
22|The browser requests an image URL. A server filesystem path must be mapped to an intentionally public resource address.
23|A fit or crop operation changes the actual image pixels to match the thumbnail shape; storing a name alone cannot do that.
24|A client can alter submitted fields, so the server must assign the intended initial pending status in its accepted insert data.
25|The requested ID must resolve to the intended task before an update can safely target it.
26|The destination must exist and permit the server to write before the handler can truthfully report a completed upload.
27|Redirecting after a successful POST makes the next ordinary refresh repeat the list GET rather than the original insertion request.
28|Validation rules combine requirements. Passing MIME checks does not cancel a failed size check.
29|Compare the submitted HTTP method and action URL with the route table to see why the receiving handler is not selected.
30|The rule checks whether the submitted value already exists in the named table column.
31|The failure branch returns the form workflow with attempted input and validation feedback instead of treating the write as successful.
32|Validation associates errors with field keys. The input name and the error lookup must identify the same field.
33|The validation error helper displays the relevant server-side field message rather than recovering old input or creating a token.
34|Old input restores the user's previous submitted title, including a rejected value that was not written to the database.
35|Update changes an existing record while preserving its identity.
36|Read retrieves existing record data without creating, changing, or removing that data.
37|After failure, the attempted title is the most useful correction value; the existing title remains the fallback.
38|An unchanged title belongs to the same record. Exclude that record from the update uniqueness comparison while still checking other records.
39|The update method selects the row by ID and applies the intended new values to it.
40|Following an ordinary link issues a GET, while deletion is a deliberate state change that needs the protected submission flow.
41|The edit form needs the existing task's saved values and identity, so resolve that selected record before rendering.
42|The old submitted value takes priority when available; otherwise the second argument supplies the saved title.
43|The ID is the explicit selected-record identifier; the data array supplies changes rather than display position.
44|The form needs multipart encoding to send its file contents through the expected upload API.
45|Inspect the action for an insert call where a selected-ID update is required; the two operations have different persistence effects.
46|The uploaded rule expresses required file presence for attachment, separately from type or size acceptance.
47|The max-size rule uses 2048 kilobytes for this field, rather than a string length or a 2 KB bound.
48|Use a deliberate protected state-changing submission, verify its CSRF token and access, and check the selected target before deletion.
49|The uploaded-file API returns the file object for the named multipart field; ordinary text getters do not supply that object.
50|The random-name method generates the server's stored filename instead of reusing the original client name.
51|The true third argument tells directory creation to create missing parent directories recursively.
52|CSRF verification and title validation protect different properties. A valid token does not establish title presence, length, or other content rules.
53|The attachment attribute must be permitted by model field protection before a normal protected write can persist its reference.
54|A file input alone is insufficient; multipart encoding is needed to include the selected bytes in the request.
55|The multipart input name is the lookup key. Both sides must use the same name to retrieve that upload.
56|A filesystem path identifies server storage. A URL identifies the resource address a browser can request.
57|The upload must pass the intended checks before it is accepted and moved into its storage destination.
58|The stored location and generated browser address must refer to the same intentionally exposed file resource.
59|Restored text values do not repopulate a browser's file selection; the visitor generally selects the file again.
60|Field protection permits attribute names. Separate validation checks values, upload properties, and the application's input requirements.
'''
CORRECT_ROWS[4]=r'''
1|Sessions connect separate requests with small stored state, such as the current visitor's authenticated identity.
2|The set method writes the named session value so later requests can retrieve it.
3|Removing a named key leaves other session values intact, unlike destroying the complete session.
4|The next request is admitted only if the login success branch saved the same key and value that the filter expects.
5|Flash data suits short-lived feedback across a redirect and its next-request lifecycle; reading it does not immediately consume it.
6|The flash-data getter retrieves the message value specifically marked for that short-lived session lifecycle.
7|A user ID gives later requests the needed identity reference without retaining the typed password or whole account table.
8|The password-hashing API creates a salted password verifier suitable for later checking with the matching verification API.
9|The verification function checks the submitted plaintext against the algorithm and salt encoded in the stored password hash.
10|The username condition selects the candidate account; the retrieved hash still needs a separate successful password check.
11|A remaining login flag can still satisfy the filter even after a separate display-name value is removed.
12|The before hook runs ahead of the controller action, allowing it to reject a guest before protected work happens.
13|The filter class implements the framework's filter interface, which defines its request and response hook contract.
14|The alias registry connects the short route filter name with the implementing filter class.
15|The route option applies its registered filter before the protected action; it does not automatically perform unrelated field or ownership validation.
16|Authentication establishes a signed-in identity. Role and record permissions require additional application checks.
17|Flash data automatically supports the intended short feedback lifecycle, unlike a normal session value retained without removal.
18|Each protected write endpoint must enforce access independently of whether the visitor can open its list page.
19|A hidden button does not stop a direct request. The receiving server endpoint must check whether the visitor is allowed.
20|An existing class is not enough: the route's short alias must map to that class in the filter configuration.
21|The before hook can redirect before the controller changes data; an after hook would be too late for the initial gate.
22|A simple login flag establishes authentication state, not permission to read or change another user's selected task.
23|A redirect creates another request. Saved session identity survives that boundary, while the action's local variables do not.
24|Removing only the preference satisfies the narrow goal while leaving authentication state available.
25|Unique usernames let the login lookup identify one candidate account rather than an ambiguous duplicate identity.
26|An existing-account login needs a matching stored user and password hash. An empty table supplies neither.
27|A direct protected request after logout tests the server-side gate rather than merely the page's button visibility.
28|The taught login workflow submits credentials to its receiving POST handler with the intended form protections rather than putting them in URLs.
29|Failed credentials must leave the visitor unauthenticated and return appropriate correction feedback.
30|A success response alone does not create continuity; the application must preserve the verified identity for later requests.
31|The authenticated user's ID identifies the current account without storing unnecessary passwords or entire collections.
32|Testing the same protected request after login checks that the filter admits an authenticated visitor as well as rejecting a guest.
33|The password column stores the password verifier; the plaintext should not be persisted as the login password value.
34|A return ends that action's execution, so flash data must be set before returning the redirect.
35|The function produces a one-way password verifier rather than decryptable storage or an automatically authenticated session.
36|The PHP constant selects the password API's default hashing algorithm, not an application password or session value.
37|Password hashing is one-way verification. Login checks a submitted password against the hash without decrypting it back to plaintext.
38|The user model in this account feature manages rows from the users table.
39|The view must read the same flash key that the controller wrote; different keys identify different values.
40|Account creation and sign-in are separate operations. A login attempt should verify an existing account instead of inserting a new one each time.
41|A reusable filter centralizes the route admission check and reduces inconsistent copies across protected controller actions.
42|A password input masks typed characters in the page; that display behavior is separate from server-side storage hashing.
43|The input type changes on-screen presentation only. The server must still create the password hash before persistent storage.
44|The where condition compares the username column, and first retrieves the matching candidate account if one exists.
45|No matching row means there is no stored password field to inspect; handle that absence before dereferencing the result.
46|Use password verification to compare submitted plaintext with the existing stored password hash.
47|The typed plaintext and its stored hash are different representations, so direct string equality is not a password verification operation.
48|Fresh password hashing can use a new salt. Verification must inspect the existing hash rather than compare two independently generated hash strings.
49|The user ID directly identifies the authenticated database row; a Boolean login flag alone does not say which user is signed in.
50|Later requests need the verified identity state, not a retained copy of the submitted password.
51|The login endpoint presents the sign-in flow for a guest who no longer has authenticated task access.
52|Masking characters does not hash them. The server still needs password hashing before persistent account storage.
53|Check authentication before protected controller work, rather than after the data or response has already been produced.
54|The after hook receives the response after the controller has run and can apply response-related processing.
55|The incoming HTTP request is represented by RequestInterface; the filter and response interfaces describe different objects.
56|A null lookup supplies no stored user hash. Reject the missing identity before attempting to read or verify that field.
57|Small identity values provide the continuity later requests need without copying excessive or sensitive account data into every session.
58|Record ownership is a separate authorization decision and does not follow automatically from a successful login.
59|The before-access gate redirects the unauthenticated visitor to login without running the protected task response or write.
60|Logout must remove the authentication state the filter actually trusts; clearing only one display key can leave that state active.
'''

CORRECT_ROWS[5]=r'''
1|The routing concept transfers between frameworks, but the receiving framework needs its own route registration syntax and APIs.
2|Presentation templates belong under `resources/views`; the unchanged query does not need a schema or model change.
3|The normal web route definitions belong in `routes/web.php` in this Laravel structure.
4|Laravel stores application HTTP controller classes in `app/Http/Controllers`.
5|Blade templates are resolved beneath `resources/views` rather than the public directory or CodeIgniter's view path.
6|`APP_URL` supplies the configured application address; it is separate from the display name, environment, and debug setting.
7|Artisan's serve command starts the Laravel application's simple local development server.
8|The view route helper directly registers a URL whose response renders the named static template.
9|The braces capture the URL component and pass its value into the closure's matching parameter.
10|The controller generator creates the PageController class file; its actions and route connections still need implementation.
11|The route-list command displays registered methods, paths, names, and handlers for inspection.
12|The handler array pairs the controller class reference with the action method to call for the matched request.
13|Associative array keys become the names of values available in the rendered view.
14|The route must point to a callable public action that actually exists on the referenced controller class.
15|Normal Blade double braces escape the value for HTML text output rather than interpreting its tags as raw markup.
16|The supplied data key is course, so escaped `$course` output reads the intended value safely as text.
17|The view-data key determines the exposed variable name, making the supplied value available as `$heading`.
18|Dot notation identifies the tasks subdirectory and show template beneath `resources/views`, without including the Blade extension.
19|The action must use the route's captured value when selecting or constructing details instead of always using a fixed ID.
20|The GET registration does not establish a POST handler for the same path; that submission needs a matching route method.
21|Installing the global installer supplies a project-creation tool. Running `laravel new` uses it to create an application.
22|A fixed displayed ID despite different captures indicates that the action is not propagating the selected parameter into its data.
23|The view helper renders the template with its data for the current response rather than generating a URL or redirect.
24|Keep database retrieval in the data layer coordinated by the controller, then let Blade display the supplied records.
25|A working text response tests route dispatch but does not exercise the intended template's file path or view variables.
26|`APP_NAME` identifies the application's configured name rather than its address or debugging behavior.
27|Database connection values vary by environment and belong in the active database configuration rather than presentation code.
28|`APP_DEBUG` directly controls whether detailed application debugging information is displayed.
29|The shell must run the command from the project containing the `artisan` entry file.
30|An application URL setting describes an address; it does not start or configure a listening server process automatically.
31|The local hostname and web-server virtual-host setup must resolve and serve the address configured in APP_URL.
32|The configuration files read the relevant environment values into application settings.
33|Artisan is Laravel's application command interface; Composer and Blade serve different package and presentation roles.
34|The controller action needs a matching route that connects an incoming request to that method.
35|Composer's run command executes the named script defined in the project's composer.json.
36|The shell must be able to find the globally installed Laravel tool through Composer's global bin directory on PATH.
37|The server cannot bind that listening port because another process already uses it; inspect the conflict or choose another port.
38|Laravel supports direct route closures and static-view routes, so a separate controller is not required for every simple response.
39|A matched route closure can return the fixed text directly without introducing a database table or Blade template.
40|The router executes the closure when its registered method and path match the incoming request.
41|CodeIgniter's explicit route configuration serves the comparable request-mapping role in `app/Config/Routes.php`.
42|The view route helper registers a URL that directly renders its configured template.
43|A generated class is only a starting file. The page still needs an implemented action and its intended route and response.
44|Escaped Blade output displays the visitor's name as text instead of allowing embedded HTML tags to affect the page.
45|A plain captured ID is only a request value. Retrieving a model requires a lookup or the appropriate binding setup.
46|The generated HTTP controller class belongs in Laravel's application controller directory, not its views or routes directory.
47|The namespace must correspond to the application HTTP controller directory: App, Http, then Controllers.
48|The selected ID must flow from the route capture through the handler into selected data and the view that displays it.
49|The list command displays the available Artisan commands rather than only HTTP route registrations.
50|The route-list command inspects the application's current HTTP route registrations.
51|The class constant supplies the controller's fully qualified class reference to the route handler array.
52|The method-name string selects the action on the referenced controller class.
53|The data argument exposes its named values to the template; it does not automatically export every local controller variable.
54|The server intentionally exposes public asset locations. Internal controller source directories do not automatically become browser CSS URLs.
55|Laravel's route inspection uses Artisan's route-list command rather than CodeIgniter's Spark command.
56|A class-based route must resolve the intended controller through the correct namespace or import before database details are relevant.
57|Blade double braces apply escaped text output to the value; raw PHP or raw Blade output does not do that automatically.
58|The raw Blade delimiters allow unescaped interpretation. Use that behavior deliberately, rather than treating untrusted text as safe HTML.
59|Without the correct import or class name, the route cannot resolve the intended controller even if a similarly named file exists.
60|Both controllers coordinate incoming requests with data operations and the response, despite differences between the frameworks' APIs.
'''
CORRECT_ROWS[6]=r'''
1|A migration records a schema change, such as creating a table or altering its columns.
2|Laravel's seeder classes are stored in `database/seeders` and supply setup or demonstration records.
3|The timestamps helper adds both conventional creation and update timestamp columns.
4|The nullable modifier permits SQL NULL for the selected column; it is different from storing an empty string or default value.
5|The migrate command applies migration files that have not yet been run in the selected database.
6|A default rollback reverses the most recent migration batch, which can contain more than one migration.
7|Fresh drops the database tables and runs migrations again; it is a destructive rebuild rather than a data-preserving repair.
8|A task seeder inserts predictable records into an already prepared schema; schema definitions belong in migrations.
9|The make-model command generates the Task model class, separately from its controller, migration, or seeder.
10|The fillable property identifies attributes permitted for mass assignment; it does not validate their values.
11|The all method retrieves the model's task records as a collection, rather than a single task or numeric count.
12|The compact helper builds a keyed array from the existing `$tasks` variable without executing another query.
13|The get method executes the filtered query and returns a collection of all its matching models.
14|A failed find-or-fail lookup throws the model-not-found exception, which normal HTTP handling turns into a 404 response.
15|Read the title from the individual Task model using its object-property access, not from the entire task collection.
16|Tinker opens an interactive application environment for inspecting models, queries, and their results during development.
17|Find-or-fail resolves the selected ID or follows the normal not-found path when the record does not exist.
18|Migrations define table structure; seeders insert records into that structure.
19|A migration file has no schema effect until it runs against the same active database that the page uses.
20|A collection contains models. Iterate or select an individual model before reading that model's title property.
21|The passed value is a Task object, so the taught property-access form uses the object operator.
22|In the standard timestamp setup, latest orders created_at descending, and get retrieves the resulting collection.
23|Counting through the active model connection checks whether that database actually contains rows before changing a working template.
24|Fresh drops tables and their contents, so it cannot preserve existing work as a routine page correction.
25|Null is not an object with a title property. Handle the missing first model before accessing its fields.
26|The optional notes column needs the nullable modifier when SQL NULL is an accepted stored value.
27|Omitting the field lets its configured false default apply; creating a row does not imply true.
28|Eloquent's standard model naming convention maps the singular Task class to the plural tasks table.
29|Compact uses an existing variable, so the controller must retrieve and assign the tasks before constructing that view-data array.
30|Unconditional seeding attempts another insert each time; existing data and constraints determine whether rows are added or rejected.
31|Reversing a schema change is not the same as restoring row contents lost when its down operation drops the table.
32|Migration execution and application queries must target the same intended connection and SQLite file to see the same schema and data.
33|The task table and columns must exist before the seeder can insert rows into them.
34|A create call uses mass assignment, so inspect the permitted model fields when an intended attribute is not accepted.
35|Retrieve models through the data layer, pass them from the controller, and use Blade to present the supplied collection.
36|Refresh uses migration rollback and replay; fresh drops tables and runs migrations. Neither is merely a web-server restart.
37|A two-branch display fallback can mislabel an unexpected status. It presents values but does not validate which values may be stored.
38|Generating the class does not insert demonstration records; a separate seed or write operation must supply those rows.
39|The fillable list permits named attributes for mass-assigned model writes.
40|Permission to assign a field does not establish valid content. Required, length, and other value constraints remain separate validation work.
41|The default table name for the singular Task model is the plural tasks name.
42|CodeIgniter models serve the comparable data-layer role, although the model APIs and property names differ.
43|Compact constructs an array containing the already assigned tasks variable under the tasks key.
44|The supplied tasks key exposes the plural `$tasks` variable in Blade.
45|The foreach directive iterates the collection so the template can display each task model.
46|A schema column establishes storage and fillable permits assignment; neither establishes the form's complete input requirements.
47|Get fetches the filtered matching models as a collection; first, count, and exists produce different result shapes.
48|The where condition selects records whose status equals pending; sorting or counting does not express that filter by itself.
49|The missing-model exception normally produces a 404 response rather than an invented task or random redirect.
50|The where call builds a query. Retrieval such as get must execute it before the controller has fetched task models.
51|Create inserts a new model record from the intended allowed attributes; the other calls retrieve existing data.
52|The conventional resource index action receives the list request and prepares the task collection response.
53|A strict comparison with the string done enters that branch only when the stored status is that exact value.
54|Dot notation resolves the tasks subdirectory and show Blade template beneath resources/views.
55|The filtered get call returns a collection of matching models, which can be empty, rather than guaranteed one-record or rendered HTML output.
56|The singular task key becomes the singular `$task` variable in the details template.
57|Tinker is the application's interactive inspection shell for evaluating model calls and checking their results.
58|Count returns a numeric row count. Gaps in primary keys do not change that count into the largest ID.
59|First can return null on an empty result. Check for a model before reading its title property.
60|Keep database retrieval in the model/controller data flow and let the view focus on presentation of the supplied records.
'''

CORRECT_ROWS[7]=r'''
1|The create endpoint displays the form; the store endpoint receives the new-record POST submission.
2|The web form needs the CSRF token expected by its enabled middleware, separately from validating the title's content.
3|The csrf directive inserts the hidden token field required by the normal protected web-form submission.
4|The HTTP Request object represents the current incoming request; an uploaded file or model represents a different component.
5|In the ordinary web-form workflow, validation failure redirects back with errors and old input before the normal write proceeds.
6|The title must be present, must be a string, and must not exceed 100 characters.
7|The error directive checks the validator's error bag for the exact title field key.
8|Implicit binding resolves the route-selected existing task, which supplies the edit form's saved data.
9|The method directive creates the hidden override that makes the HTML POST submission an effective PATCH request.
10|Old submitted input is preferred after failure; the saved model title is the fallback when no old input exists.
11|For a file, the numeric maximum is a size bound in kilobytes, not a pixel or filename-length bound.
12|The storage method returns the path reference assigned on that disk, which the model can retain for later access.
13|The storage-link command creates the standard local link from public/storage to the public disk's storage directory.
14|Successful validation returns the accepted data array; persistence and record authorization remain deliberate separate operations.
15|The request generator creates a Form Request class where reusable or longer validation definitions can live.
16|Keep the old usable file until the replacement has been validated, stored, and successfully associated with the record.
17|Invalid input returns to the form with correction feedback and the attempted values rather than being saved as success.
18|The error block looks up name, but the validated input is title. Use the same field key on both sides.
19|The saved path already contains the attachments directory, so prefix only storage when building this public-disk URL.
20|Deleting first loses the original bytes even if later validation, storage, or persistence fails; old input cannot recreate those bytes.
21|Draft 2 is the failed attempted input and therefore takes priority; Draft 1 remains the model fallback.
22|No optional replacement means retain the existing reference and file, unless a separate explicit removal action was requested.
23|Form Request authorization and validation are separate. A false authorize result rejects the request before the controller proceeds.
24|Use the intended validated fields with the model's write rules, rather than bypassing the validation result with all raw input.
25|Copied package code must match the installed version and class import; changing validation rules does not resolve an unavailable class API.
26|Resolve the selected record and access first, validate input, update intended fields, and then return success through the redirect.
27|The application enforces its own 100-character maximum before the database write, even though the column can hold more.
28|Deletion must use the same disk and relative-path interpretation as storage to remove the intended file.
29|Request injection gives access to incoming data but does not automatically validate, authorize, save, or process that data.
30|The edit workflow begins with the selected existing record, which supplies the initial values and target identity.
31|The standard tasks.update route receives an existing task's update submission; edit displays its form and store creates a new task.
32|A normal HTML form submits POST, while the hidden override supplies PATCH and the CSRF field provides the separate request token.
33|The route capture name task matches the typed action parameter, allowing the framework to resolve that Task model.
34|Binding resolves the selected model instance. It does not itself establish ownership permission or return validated request fields.
35|Finding a task proves existence, not the current user's permission to change it. Check record access separately.
36|Both frameworks use old-input helpers to restore a previous submitted value after a failed form submission.
37|The instance update targets that selected model and applies permitted attributes from the accepted data.
38|The matching route parameter and model type resolve one existing task or the normal not-found path, not ownership permission.
39|HTML submits POST; Laravel reads the hidden method override to route it as PATCH.
40|The method directive generates the effective PATCH override rather than the token or validation feedback.
41|Method spoofing selects the effective HTTP verb. It does not perform CSRF verification or replace the separate csrf token field.
42|Multipart encoding carries the selected file bytes in the upload form's request.
43|Binding establishes which task exists. The server must still decide whether this authenticated user may modify that owner's task.
44|The image rule restricts an accepted nonnull upload to the supported image types, separately from presence and size rules.
45|The mimes rule checks a content-derived MIME type corresponding to its listed extensions, rather than trusting a renamed filename alone.
46|For this file rule, the maximum is measured in kilobytes rather than image dimensions or text length.
47|Has-file checks the upload field's presence. Validation and accepted-upload handling still decide whether storage may proceed.
48|A nullable image field can accept no replacement. The absence does not require deleting the existing file or relaxing other fields.
49|Laravel's numeric uploaded-file size limits use kilobytes; the same max rule has different meanings for other validated data types.
50|Store returns the assigned relative storage path rather than a complete browser URL or a saved database model.
51|The standard local public link exposes the public disk at public/storage, not every private disk or internal application file.
52|The form needs multipart encoding to make the selected file available through the uploaded-file API.
53|Test the attachment reference itself before emitting its image element; an existing task ID does not guarantee an attachment.
54|Remove the old file after successful replacement storage and persistence so a failed replacement does not destroy the prior usable file.
55|Store the returned relative path as the persistent reference, then generate the appropriate browser URL separately.
56|The cover operation prepares the requested square crop for display; its dimensions are not a validation file-size limit.
57|The public URL needs the configured public storage link to connect that address with the file's disk location.
58|Rules defines the Form Request constraints. Authorization, validated results, and custom messages have separate methods.
59|Inject the generated Form Request into the receiving action so its checks run before the controller's normal write path.
60|A database transaction covers database operations. File deletion and storage need explicit coordination and recovery handling.
'''
CORRECT_ROWS[8]=r'''
1|The resource registration creates the conventional CRUD method-and-path map for the task controller.
2|Registration connects requests to action names. The controller still needs the validation, access checks, and save behavior for those actions.
3|The conventional resource destroy action handles the selected task's DELETE request.
4|Create displays the new-task form; store receives and saves the later submitted data.
5|The standard resource update route accepts PUT or PATCH for the selected record.
6|PATCH requests changes to the selected existing task, which the controller applies after the intended access and input checks.
7|The selected-record GET route maps to show, which prepares the response for that task.
8|The POST form carries the CSRF token and a DELETE method override so dispatch reaches the protected destroy action.
9|Authentication middleware requires a signed-in identity. Record-level permission and input validation still need their own checks.
10|A user owns many tasks, so the User model defines a has-many task relation used for related task creation.
11|Starting from the current user's relationship scopes ownership; latest orders that scope by newest creation time before retrieval.
12|Task::all is a global query. A successful login does not automatically add the current user's ownership condition.
13|The authenticated user's relationship supplies the intended ownership association instead of trusting a client-submitted owner ID.
14|The content method selects the mailable's content view, such as its Markdown template; recipient and dispatch are separate.
15|The call selects the authenticated recipient and then sends the constructed task-completion mailable.
16|The conjunction requires both a saved status change and a destination of done, excluding later edits where done stays unchanged.
17|A completion trigger must identify the saved transition into done, rather than any record merely remaining in that state.
18|An independent show lookup must enforce selected-record access even when the index query is scoped to the current user.
19|Checking the saved status change excludes title-only updates to a task that was already done.
20|The owner is one user with many task rows, each referencing that user through its foreign key.
21|The attribute changed, but its new value is pending. The combined condition requires the new value to be done.
22|A model transition condition does not provide durable deduplication, successful transport, or exactly-once inbox delivery under every failure and retry.
23|The redirect's status key is a flash-feedback message; the task object's status is a separate persisted workflow attribute.
24|Unintended duplicate registrations can leave confusing effective endpoints. Keep the intended protected map and inspect the registered routes.
25|Authentication scaffolding supplies the sign-in feature, while the task feature still needs its own validation, permissions, and operations.
26|A mailable can render correctly while transport fails. Working delivery needs a reachable usable service and valid mail settings.
27|Each unguarded record action can still be called directly; an edit-only access check does not protect destroy or upload automatically.
28|Latest applies newest-created ordering in the standard timestamp setup; retrieval remains a separate query operation.
29|Latest changes ordering only. A global Task query still needs an explicit current-user condition or relationship scope.
30|Create presents the empty new-record form rather than saving a submission or editing an existing record.
31|The from-name setting controls the sender's displayed label rather than the server or connection password.
32|Selected-record binding supplies one existing Task model to the show or edit action.
33|Auth middleware establishes a signed-in visitor before the action. Ownership, field validity, and write success remain separate concerns.
34|Composer's development flag records the package in development dependencies; it does not select a controller or seed option.
35|The argument explicitly supplies the authenticated user's email as the recipient; the configured sender address has another role.
36|Npm installs the JavaScript dependencies declared for the scaffold, separately from Composer's PHP dependencies and database migrations.
37|Choosing the Markdown view establishes how the email content is rendered; it neither authorizes the record nor dispatches the message by itself.
38|The middleware group applies the authentication gate to the routes defined inside it.
39|A generated or emailed task URL identifies a destination but does not grant access to the record at that destination.
40|A CodeIgniter authentication filter supplies the comparable reusable request gate before protected controller work.
41|The user_id column references the owner; the task's own ID separately identifies the task record.
42|The user's has-many relationship represents the collection of tasks associated with that user.
43|Creating through the authenticated relationship associates the new task with that verified user instead of a visitor-chosen owner.
44|The current user's tasks relationship starts a query with the intended user association rather than the global task collection.
45|Every selected-record read or write endpoint needs its intended access restriction, independently of the private list.
46|The mailer setting chooses SMTP as the transport driver; the host setting separately names the outgoing server.
47|Mail host identifies the outgoing server hostname, separately from its port, sender address, and authentication username.
48|The from-address setting supplies the sender email address; transport host and username are separate configuration values.
49|Placeholder settings do not establish a working mail account or reachable service, regardless of a valid completion trigger.
50|The generated PHP mailable class belongs in app/Mail; its Blade content template belongs in the views directory.
51|The dotted Markdown view identifier resolves to the matching nested Blade template beneath resources/views.
52|Publishing the laravel-mail vendor tag copies the mail views for customization rather than exposing a storage disk or sending a message.
53|Constructor property promotion receives the Task argument and makes it available as the mailable's public task property.
54|Content defines the message presentation. Recipient selection and a send or queue operation perform the separate dispatch workflow.
55|The mail message component provides the standard Markdown email wrapper around its content.
56|The named show route generates the display URL for the selected task; create, store, and destroy serve different operations.
57|Sending first can announce a completion that a later failed update never persisted. Confirm the write before making that claim.
58|The chained with call flashes session feedback for the redirected request; it does not update the model's status column.
59|The condition combines a saved attribute change with the intended destination state, targeting the transition into done.
60|The local condition is not an exactly-once delivery mechanism; retries and partial failures need separate durable delivery design.
'''

# These revisions remove overlapping valid answers or narrow an imprecise
# question. New IDs keep old attempts from being graded against a changed item.
FIXES={
 (1,11):{'prompt':'Which general-purpose placeholder accepts one nonempty path component, including letters, digits, and hyphens, but never a slash?'},
 (1,49):{'prompt':'Which general-purpose placeholder accepts one path component containing letters, digits, or hyphens while excluding slashes?'},
 (1,52):{'prompt':'Which route placeholder restricts the captured value to alphabetic characters?'},
 (2,52):{'choices':{1:'getInsertID()'}},
 (2,54):{'prompt':'Which dedicated Query Builder method sets a result-count limit before retrieval?'},
 (4,6):{'choices':{1:'has()'}},
 (6,13):{'prompt':'Which method retrieves a collection of all models matching Task::where(...)->orderBy(...)?'},
 (6,47):{'prompt':'Which method retrieves all matching Eloquent models as a collection after a filtered query?'},
}
CORRECT={
 (1,1):'A framework supplies reusable routing, database, validation, and request-handling tools. Reusing these tools reduces repeated infrastructure work, while the developer still writes the application-specific behavior.',
 (1,11):'`(:segment)` matches a nonempty component without a slash. Unlike numeric or alphabetic placeholders, it also accepts the mixed characters required here.',
 (1,49):'Use `(:segment)` for the mixed single component. It excludes slashes without restricting the value to only numbers or only letters.',
 (1,52):'`(:alpha)` expresses the alphabetic-only restriction. A general segment can contain letters too, but does not enforce that restriction.',
 (2,52):'`findAll()` executes the filtered model query and returns the matching rows. `first()` returns one row, a count returns a number, and `getInsertID()` reports insertion metadata.',
 (2,54):'`limit()` adds the dedicated result-count bound to the query chain. `findAll()` can also accept a bound at retrieval, but the question asks for the separate Query Builder step before retrieval.',
 (4,6):'`getFlashdata()` reads a value specifically marked as flash data. `has()` checks existence, `setFlashdata()` writes it, and `remove()` deletes it. Reading a flash message does not immediately erase it during that request.',
 (6,13):'`get()` executes the query and returns a collection of its matching models. The other methods can also execute queries, but return one model, a count, or an existence result instead.',
 (6,47):'Use `get()` when the next step needs a collection of matching models. `first()`, `count()`, and `exists()` return different result shapes, even though each can execute a query.',
}

def build():
    bank_path=ROOT/'tools/question-bank.json'
    questions=json.loads(bank_path.read_text(encoding='utf-8'))
    authored={}
    for module,block in REASONS.items():
        rows={}
        for line in block.strip().splitlines():
            pieces=line.split('|')
            assert len(pieces)==4,(module,pieces)
            number=int(pieces[0]);assert number not in rows
            rows[number]=pieces[1:]
        assert set(rows)==set(range(1,61)),module
        authored[module]=rows
    correct={}
    for module,block in CORRECT_ROWS.items():
        rows={}
        for line in block.strip().splitlines():
            number,explanation=line.split('|',1)
            assert int(number) not in rows
            rows[int(number)]=explanation.replace('\\\\','\\')
        assert set(rows)==set(range(1,61)),module
        correct[module]=rows
    assert len(questions)==480 and set(authored)==set(correct)==set(range(1,9))
    for q in questions:
        number=int(re.search(r'q(\d+)',q['id'])[1]);key=(q['module'],number)
        fix=FIXES.get(key)
        if fix:
            if 'prompt' in fix:q['prompt']=fix['prompt']
            for index,value in fix.get('choices',{}).items():q['choices'][index]=value
            # Re-running the build keeps the same revised identity.
            q['id']=f'm{key[0]}q{number}-feedback-v3'
        q['explanation']=CORRECT.get(key,correct[key[0]][number])
        reasons=authored[key[0]][number]
        if key==(2,52):reasons[0]='This reports the last inserted primary-key value, not the rows matching the read query.'
        assert q['answer']==q['choices'][0]
        assert all(len(reason.strip())>=12 for reason in reasons),q['id']
        q['choiceExplanations']=dict(zip(q['choices'],[q['explanation'],*reasons]))
        assert len(q['choiceExplanations'])==4,q['id']
    bank_path.write_text(json.dumps(questions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Added correct-answer and three option-specific explanations to all 480 questions. Revised eight ambiguous items.')

if __name__=='__main__':build()
