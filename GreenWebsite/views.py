from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Product, UserProfile, ReviewRating, Cart, CartItem, Articles
from django.contrib import messages
from . import forms
from django.contrib.auth.views import PasswordResetView
from .forms import ProductForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

def send_test_email(request):
    send_mail(
        'Testing Email Sending',  # Subject
        'This is a test email sent from Django.',  # Message
        'greenleafhub00@example.com',  # From email address
        ['cherrydaniel11@gmail.com'],  # To email addresses (can be a list)
        fail_silently=False,  # Raise an exception if sending fails
    )
    return render(request, 'email_sent.html')


def dashboard(request):
    products = Product.objects.all()
    return render(request, 'dashboard.html', {'products': products})


# Create your views here.


def signup_view(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f'{field}: {error}')
    else:
        form = forms.UserRegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'{username} logged in successfully')
                return redirect('dashboard')  # Redirect to dashboard on successful login
            else:
                # Handle invalid credentials
                form.add_error(None, 'Invalid username or password.')
                messages.warning(request, f'Invalid username or password.')
    else:
        form = forms.LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('dashboard')


class CustomPasswordResetView(PasswordResetView):
    form_class = forms.CustomPasswordResetForm
    template_name = 'registration/password_reset.html'


def product(request, pk):
    product = Product.objects.get(id=pk)
    reviews = ReviewRating.objects.filter(product=product)
    return render(request, 'product.html', {'product': product, 'reviews': reviews})


def product_gallery(request):
    products = Product.objects.all()
    return render(request, 'product_gallery.html', {'products': products})


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = forms.ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = forms.ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


def add_cart(request, pk):
    pass


@login_required
@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    if request.method == 'POST':
        # Your logic for processing the form and adding a product
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, redirect to the product list page after adding the product
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_product(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)

    except Exception as e:
        print(e)
        return render(request, 'error.html', {'message': 'Product not found'})

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})


# @login_required(login_url='/login/')
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#     if not created:
#         cart_item.quantity += 1
#     cart_item.save()
#     return redirect('cart')


@login_required
def view_cart(request):
    cart_items = CartItem.objects.all()
    cart_items_with_totals = []
    cart_subtotal = 0

    for item in cart_items:
        total_price = item.product.price * item.quantity
        cart_items_with_totals.append({
            'product': item.product,
            'quantity': item.quantity,
            'total_price': total_price
        })
        cart_subtotal += total_price

    cart_grand_total = cart_subtotal  # Add additional calculations for discounts, etc., if needed

    context = {
        'cart_items': cart_items_with_totals,
        'cart_subtotal': cart_subtotal,
        'cart_grand_total': cart_grand_total,
        'is_cart_empty': len(cart_items) == 0
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    #cart_items_count=CartItem.objects.all().size()
    cart_items_count = CartItem.objects.all().count()
    messages.success(request, f'Product {product.name} added to cart successfully.')
    print("manasa", cart_items_count)
    # return redirect( '/dashboard', {'cart_items_count': cart_items_count})
    return redirect(url)


@login_required
def payment_view(request):
    return render(request, 'payment.html')


@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('cardNumber')
        expiry_date = request.POST.get('expiryDate')
        cvv = request.POST.get('cvv')
        card_name = request.POST.get('cardName')

        # Process the payment here
        # You can use a payment gateway API like Stripe, PayPal, etc.

        # For simplicity, let's assume the payment is successful
        # For simplicity, let's assume the payment is successful
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_items.delete()
        return render(request, 'payment_success.html')

    return redirect('payment_page')


def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Product.objects.filter(name__icontains=query)
        print(results)

    return render(request, 'dashboard.html', {'query': query, 'products': results})


# article and contact-us related methods from here on
# @login_required()
# def articles(request):
#     # dummy_content = [{"title": "My Updated Post", "content": "My first updated post!\r\n\r\nThis is exciting!", "user_id": 1}, {"title": "A Second Post", "content": "This is a post from a different user...", "user_id": 2}, {"title": "Top 5 Programming Lanaguages", "content": "Te melius apeirian postulant cum, labitur admodum cu eos! Tollit equidem constituto ut has. Et per ponderum sadipscing, eu vero dolores recusabo nec! Eum quas epicuri at, eam albucius phaedrum ad, no eum probo fierent singulis. Dicat corrumpit definiebas id usu, in facete scripserit eam.\r\n\r\nVim ei exerci nusquam. Agam detraxit an quo? Quo et partem bonorum sensibus, mutat minimum est ad. In paulo essent signiferumque his, quaestio sadipscing theophrastus ad has. Ancillae appareat qualisque ei has, usu ne assum zril disputationi, sed at gloriatur persequeris.", "user_id": 1}, {"title": "Sublime Text Tips and Tricks", "content": "Ea vix dico modus voluptatibus, mel iudico suavitate iracundia eu. Tincidunt voluptatibus pro eu? Nulla omittam eligendi his ne, suas putant ut pri. Ullum repudiare at duo, ut cum habeo minim laudem, dicit libris antiopam has ut! Ex movet feugait mea, eu vim impetus nostrud cotidieque.\r\n\r\nEi suas similique quo, his simul viris congue ex? Graeci possit in est, ne qui minim delectus invenire. Mei ad error homero maluisset, tacimates assentior per in, vix ut vocent accusata! Mei eu inermis pericula patrioque? Debet denique sea at, ad cibo reformidans theophrastus per, cu inermis maiestatis vim!\r\n\r\nUt odio feugiat voluptua est, euismod volutpat qualisque at sit, has ex dicit ornatus inimicus! Eu ferri laoreet vel, dicat corrumpit dissentias nec in. Illum dissentiunt eam ei, praesent voluptatum pri in? Ius in inani petentium, hinc elitr vivendum an vis, in vero dolores electram ius?", "user_id": 1}, {"title": "Best Python IDEs", "content": "Elit contentiones nam no, sea ut consul adipiscing. Etiam velit ei usu, sonet clita nonumy eu eum. Usu ea utroque facilisi, cu mel fugit tantas legimus, te vix quem nominavi. Prima deserunt evertitur ne qui, nam reprimique appellantur ne.", "user_id": 1}, {"title": "Flask vs Django - Which Is Better?", "content": "Ei dicta apeirian deterruisset eam, cu offendit invenire pri, cu possim vivendo vix? Nam nihil evertitur ad, ne vim nonumy legendos iracundia. Vix nulla dolorem intellegebat ea? Te per vide paulo dolor, eum ea erant placerat constituam? Dolores accumsan eum at.\r\n\r\nInteresset consequuntur id vix. Eam id decore latine, iusto imperdiet ei qui. In ludus consul reformidans eam. Nec in recusabo posidonium, cu tantas volumus mnesarchum pro. Nam ut docendi evertitur, possim menandri persecuti ne sed, cum saepe ornatus delenit ei?\r\n\r\nIn mel debet aliquam. In his etiam legere, doming nominavi consetetur has ad, decore reprimique ea usu. Eam magna graeci suavitate cu, facete delenit cum ne. Ponderum evertitur tincidunt ei mel, ius ei stet euismod docendi.", "user_id": 2}, {"title": "You Won't Believe These Clickbait Titles!", "content": "Cu justo honestatis mel, pro ei appareat mediocrem suavitate. No his omnis ridens. Ludus ornatus voluptatum mei ut, an mentitum noluisse forensibus cum. Eam affert pertinax consequuntur ei, nisl zril meliore te vis? Ad animal persius concludaturque vix, eu graece audiam mel.\r\n\r\nVitae libris mentitum pri in. Cu rebum veritus sea, ex usu consul dolorum, pro tale maluisset consulatu ut. Quo ad clita persius ancillae. Vel illud blandit at, vel eu hinc graeco, usu doctus praesent ea! Vim rebum deserunt ex.\r\n\r\nIus lorem omittam id, est suavitate definitionem ad! Id vim insolens tacimates, pri at decore causae. Ex duo bonorum repudiandae? Vix no vidit facete impedit. An oportere indoctum eam.", "user_id": 2}, {"title": "These Beers Will Improve Your Programming", "content": "Sanctus senserit vis id, ut eum iuvaret invidunt constituam? Nonumes facilis mei an, ad elit explicari persequeris pri, dico recusabo quo id? At mea lorem repudiandae. Sed causae sensibus forensibus ea, ne ornatus suscipiantur consectetuer mel, affert nostro nominati cu qui. Te sanctus constituto est, corrumpit pertinacia eos et, mei libris persequeris an.\r\n\r\nQuo fuisset sensibus in. Ad est assueverit adversarium, viris aperiri numquam est ad. Pro mediocrem iudicabit ei! Cu aperiam diceret sit.", "user_id": 1}, {"title": "List of PyCon 2018 Talks", "content": "Has ea verear adolescens, elit justo constituam duo in, vix an copiosae contentiones. Eos persius consequuntur no, esse percipit cum ea, per modus harum praesent at. Et clita delenit luptatum usu? No cum interpretaris concludaturque. Congue pertinax ea mea.\r\n\r\nBrute iracundia philosophia ei quo, nam at adhuc idque, ex dolor homero mei. No mea affert tacimates pertinacia, in maluisset dissentias consectetuer mei, vel no aliquam splendide. In has nobis vocent adipisci? Pri clita delicata in, iusto viris scripserit vim in? Sit in lorem complectitur. Sanctus eloquentiam eum ut, et sumo apeirian mea? Vim te affert populo voluptaria, utinam consul ad duo.", "user_id": 1}, {"title": "How Dogs in the Workplace Boosts Productivity", "content": "Has ea verear adolescens, elit justo constituam duo in, vix an copiosae contentiones. Eos persius consequuntur no, esse percipit cum ea, per modus harum praesent at. Et clita delenit luptatum usu? No cum interpretaris concludaturque. Congue pertinax ea mea.\r\n\r\nBrute iracundia philosophia ei quo, nam at adhuc idque, ex dolor homero mei. No mea affert tacimates pertinacia, in maluisset dissentias consectetuer mei, vel no aliquam splendide. In has nobis vocent adipisci? Pri clita delicata in, iusto viris scripserit vim in? Sit in lorem complectitur. Sanctus eloquentiam eum ut, et sumo apeirian mea? Vim te affert populo voluptaria, utinam consul ad duo.", "user_id": 1}, {"title": "The Best Programming Podcasts", "content": "Vidisse malorum platonem vel no. Persecuti adversarium ut sit, quo et stet velit mundi! Id per homero expetenda. Est brute adipisci et!\r\n\r\nLorem aliquip has in, quo debet ceteros sadipscing ne! An sea odio ornatus inermis, an per ipsum persecuti dissentiunt, no mea bonorum pertinacia delicatissimi? Ne sumo diceret mea, percipit repudiare eam no! Pro et lorem accommodare. At eius novum phaedrum mei?\r\n\r\nIgnota conclusionemque mei no, eam ut munere fierent pertinacia. Ea enim insolens gloriatur duo, quis vituperatoribus pro no! Ei sed bonorum reprehendunt, aliquam nominavi his et. Magna decore referrentur id nec. Cum rebum ludus inimicus no, id cum iusto labores maluisset!\r\n\r\nQui no omnis numquam apeirian, et vide interesset cum? Et nec nulla signiferumque. Enim instructior eos ei, solum tollit phaedrum his in? No vix malorum ornatus, cu quo hinc everti iracundia, essent eruditi efficiendi ut nam. Altera saperet usu eu, errem expetenda cu duo. Has dolor splendide et, no mel cibo ancillae voluptatum, mutat antiopam deterruisset ei qui. Dolores scripserit concludaturque est id, ea animal facilisi splendide qui, quo at animal voluptua instructior.\r\n\r\nMeis voluptatum eu eum.", "user_id": 1}, {"title": "Tips for Public Speaking", "content": "Ex eam doctus accommodare. Ut oratio vivendo intellegebat qui. Ius ne doming petentium. Pri congue delectus ad, accumsan molestiae disputando te mea. Nam case inani eligendi at, per te esse iudico. Feugiat patrioque mei ad, harum mundi adversarium an per!\r\n\r\nAncillae verterem eleifend his at? Nam vidit iusto petentium at, vis nusquam dissentias cu, etiam doctus adversarium eam no. At alterum definiebas efficiantur eos, pro labitur vituperatoribus ne, eu odio legere vim. Ad nec verear appellantur? Ad qui vulputate persequeris.", "user_id": 2}, {"title": "Best Programmers Throughout History", "content": "Mel nulla legimus senserit id. Vim purto tractatos in, te vix error regione, erant laudem legere an vel. Falli fierent ius ex! In legere iriure est, id vis prima maluisset, purto numquam inimicus ut eos! In duo antiopam salutatus, an vel quodsi virtute definitiones.\r\n\r\nEst te sumo voluptaria, ius no putant argumentum, alienum ocurreret vim cu? Volumus democritum no vel, virtute commune an est. Vel te propriae lobortis rationibus, no eum odio neglegentur? Duo an sumo ignota latine! Nec mazim aperiam percipitur eu, id his dicit omnium.", "user_id": 2}, {"title": "How To Create A YouTube Channel", "content": "Sit et novum omnes. Nec ea quas minim tractatos, usu in aperiam mentitum necessitatibus, ut omnis equidem moderatius quo. Eos ad putent aeterno praesent. Eos omnium similique id, his accommodare philosophia at. Causae lucilius similique in mea, ut regione tritani voluptatibus mel! At possim offendit eum, aeque denique prodesset pro te?\r\n\r\nAt pro quem laudem. Et agam democritum eos? Ea quod probatus usu, no ferri fabulas cotidieque mei? Numquam nusquam quo in, quo et molestiae complectitur. Nihil semper ei qui.\r\n\r\nModo omnes forensibus duo ex, te est diceret bonorum labores! Magna ponderum eos ea. Cu vim diceret mnesarchum, graeci periculis in vis. Est no iriure suavitate!", "user_id": 2}, {"title": "How I Record My Videos", "content": "Ad vel possim delicatissimi, delectus detraxit per cu. Ad pri vidit modus altera! In erat complectitur sit, quo no nostro insolens? Aliquam patrioque scribentur quo ad, partem commune eos at. Eius vivendo comprehensam has ne, sea ne eros mazim oratio. Soluta populo te duo, ne pro causae fabulas percipitur, feugiat.", "user_id": 1}, {"title": "Python and Physics", "content": "Agam mediocritatem sed ex, fabellas recusabo dissentias vix te. No principes consequat inciderint pri, ea mundi affert persecuti mea, ne usu veri regione nostrum! An tibique dissentiet referrentur pro, ridens temporibus eu est! Ius ne omnes affert rationibus, ut detraxit qualisque usu. Accusamus reformidans sea id?\r\n\r\nEu aliquip gloriatur mei. Qui ad sint scripserit? Te instructior definitiones mel, sale mutat everti at his. Ea mea quot recusabo philosophia. Et nam quod adipisci, quo atqui appetere recusabo id, detraxit inimicus vim.", "user_id": 1}, {"title": "Just A Few More Healines Should Do It", "content": "Duo at tibique commune vulputate, ex facilis tacimates disputationi mei. Mel eu inani prompta labores! Audire omnesque offendit ex eos. An ferri accusata his, vel agam habeo maiestatis ex, eam mutat iisque concludaturque ut. Ut tamquam minimum partiendo vim. An nam vidit doming graecis.\r\n\r\nSingulis abhorreant his in, et altera audiam feugiat mei. Pri eius dolor persequeris id! Nam ea dolorem expetendis, idque everti suscipit qui te, noster repudiare dignissim per ex? No vim iriure tibique comprehensam, per utamur consequat.", "user_id": 1}, {"title": "Music To Listen To While Coding", "content": "Feugait reprimique eu mel, te eum dico electram. Nam no nemore cotidieque. Vim cu suas atqui dicunt. Id labitur dissentiunt per, ignota maiorum pri no? Clita altera sanctus ex his!\r\n\r\nAt alia electram reprehendunt eam, sea te volumus quaestio. Commodo voluptua senserit ius ne, eu enim disputationi eam? Id pri omnium blandit, nullam denique nec no? Sapientem vituperata sit et, nisl facilisis periculis in est. Elaboraret accommodare id vel? Cibo eripuit ut has, sed cu liber invidunt.\r\n\r\nEi pro vide quas dolorum, sea no fugit sanctus neglegentur. Sit feugait disputationi ne. Id diceret periculis nec, sint nonumes in sea, cum.", "user_id": 1}, {"title": "5 Tips for Writing Catchy Headlines", "content": "Ea homero possit epicuri est, debitis docendi tacimates cu duo? Ad lorem cetero disputando pri, veniam eruditi tacimates per te.", "user_id": 2}, {"title": "The Rise of Data Science", "content": "Per omittam placerat at. Eius aeque ei mei. Usu ex partiendo salutandi. Pro illud placerat molestiae ex, habeo vidisse voluptatum cu vel, efficiendi accommodare eum ea! Ne has case minimum facilisis, pertinax efficiendi eu vel!\r\n\r\nEt movet semper assueverit his. Mei at liber vitae. Vix et periculis definiebas, vero falli.", "user_id": 2}, {"title": "Best Videos For Learning Python", "content": "Mei ei mazim dicunt feugait? Ludus mandamus ne est, per ne iusto facilisis moderatius! Has agam utamur ad! Ius reque aeterno cu, fabellas facilisi repudiare eu sit, te cibo convenire similique est. Ea cum viderer imperdiet liberavisse.\r\n\r\nPro minim iuvaret ad. No nam ornatus principes euripidis, at sale vituperatoribus eos, eros regione scripserit id mea. Has ne inermis nostrum, quo tantas melius dissentias at! Ut vim tibique omnesque. An mel modo ponderum, eum at probo appetere imperdiet? Natum quaeque intellegebat per ex. Cu viris clita sit?\r\n\r\nReque menandri dissentias sed ne, no tota nonumes eos, vix in tempor maiestatis erant.", "user_id": 1}, {"title": "Top 10 Python Tips and Tricks", "content": "Pro minim iuvaret ad. No nam ornatus principes euripidis, at sale vituperatoribus eos, eros regione scripserit id mea. Has ne inermis nostrum, quo tantas melius dissentias at! Ut vim tibique omnesque. An mel modo ponderum, eum at probo appetere imperdiet? Natum quaeque intellegebat per ex. Cu viris clita sit?\r\n\r\nReque menandri dissentias sed ne, no tota nonumes eos, vix in tempor maiestatis erant.", "user_id": 1}, {"title": "Top 5 YouTube Channels For Learning Programming", "content": "Quo inani quando ea, mel an vide adversarium suscipiantur. Et dicunt eleifend splendide pro. Nibh animal dolorem vim ex, nec te agam referrentur. Usu admodum ocurreret ne.\r\n\r\nEt dico audire cotidieque sed, cibo latine ut has, an case magna alienum.", "user_id": 2}, {"title": "My Latest Updated Post", "content": "Erat expetenda definitionem id eos. Semper suscipit eum ut, eum ex nemore copiosae. Nam probatus pertinacia eu! No alii voluptua abhorreant nec, te pro impedit concludaturque, in sea malis torquatos disputationi! Nam te alii nobis ponderum, ei fugit accusamus pro.\r\n\r\nCongue salutandi ex eam! Mei an prima consulatu, erat detracto eu quo? Vim ea esse utinam efficiantur, at noster dicunt.", "user_id": 1}]
#     context = {"posts": Articles.objects.all()}
#     return render(request, 'articles/article-home.html', context)

class ArticleListView(ListView):
    model = Articles
    template_name = "articles/article-home.html"  # model_List.html is the default but since we built it already, we will proceed to change
    context_object_name = "posts"  # the default will be object
    ordering = ['-date_posted']
    paginate_by = 5


class ArticleDetailView(DetailView):
    model = Articles
    template_name = "articles/articles_detail.html"


class ArticleCreateView(LoginRequiredMixin, CreateView): # mixin instead of the loginrequire decorator
    model = Articles
    fields = ['title', 'content']
    template_name = 'articles/articles_form.html'

    def get_success_url(self):
        return reverse("article-detail", kwargs={'pk': self.object.pk})
    # There is another way of doing it and it is present in the present(Commented) in the Articles Models class
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # mixin instead of the loginrequire decorator
    model = Articles
    fields = ['title', 'content']
    template_name = 'articles/articles_form.html'

    def get_success_url(self):
        return reverse("article-detail", kwargs={'pk': self.object.pk})
    # There is another way of doing it and it is present in the present(Commented) in the Articles Models class
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self): # this is to check and pass if the article is of the logged in user itself
        article = self.get_object()
        if article.author == self.request.user:
            return True
        return False

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articles
    template_name = "articles/article_delete_confirm.html"
    success_url = '/article-home/'
    def test_func(self): # this is to check and pass if the article is of the logged in user itself
        article = self.get_object()
        if article.author == self.request.user:
            return True
        return False

class UserArticleListView(ListView):
    model = Articles
    template_name = "articles/user-articles.html"  # model_List.html is the default but since we built it already, we will proceed to change
    context_object_name = "posts"  # the default will be object
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Articles.objects.filter(author=user).order_by('-date_posted')