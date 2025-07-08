from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()


class PlaylistUltimato:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("lang=pt-BR")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(
            self.driver,
            10,
            poll_frequency=1,
            ignored_exceptions=[  
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException,
            ],
        )
        self.email = os.getenv("SPOTIFY_EMAIL")
        self.senha = os.getenv("SPOTIFY_SENHA")
        self.link_spofity = "https://open.spotify.com/"
        self.DeveUsarLoginFacebook = True
        if not self.email or not self.senha:
            raise ValueError("As variáveis de ambiente SPOTIFY_EMAIL e SPOTIFY_SENHA devem estar definidas no arquivo .env")

    def Start(self):
        self.driver.get(self.link_spofity)
        self.LoginSpotify()
        self.LogarComEmail()
        self.GerarPlaylist()

    def LoginSpotify(self):
        print("Loggando no Spotify")
        entrar_elements = self.driver.find_elements(By.XPATH, '//*[text()="Entrar"]')
        print("Quantidade de elementos 'Entrar':", len(entrar_elements))
        for el in entrar_elements:
            print("Tag:", el.tag_name, "Visível:", el.is_displayed())
        login_button = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (By.XPATH, '//button[.//span[text()="Entrar"]]')
            )
        )
        login_button.click()

    def LogarComEmail(self):
        # Preencher e-mail/usuário
        campo_email = self.wait.until(CondicaoExperada.element_to_be_clickable((By.ID, 'login-username')))
        campo_email.send_keys(str(self.email))
        time.sleep(1)

        # Clicar no botão de avançar/próximo
        botoes = self.driver.find_elements(By.TAG_NAME, 'button')
        print("Botões encontrados após preencher e-mail:", len(botoes))
        for b in botoes:
            print("Texto:", b.text, "Type:", b.get_attribute("type"), "Visível:", b.is_displayed())
        botao_avancar = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (By.XPATH, '//button[.//span[normalize-space(text())="Continuar"]]')
            )
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", botao_avancar)
        time.sleep(0.5)
        botao_avancar.click()
        time.sleep(2)

        # Clicar no botão 'Entrar com senha', se existir
        try:
            botao_entrar_com_senha = self.wait.until(
                CondicaoExperada.element_to_be_clickable(
                    (By.ID, 'google-recaptcha-v3')
                )
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", botao_entrar_com_senha)
            time.sleep(0.5)
            botao_entrar_com_senha.click()
            print("Botão 'Entrar com senha' clicado.")
        except Exception as e:
            print("Botão 'Entrar com senha' não encontrado ou não necessário.")

        # Agora esperar o campo de senha aparecer
        campo_senha = self.wait.until(CondicaoExperada.element_to_be_clickable((By.ID, 'login-password')))
        campo_senha.send_keys(str(self.senha))
        time.sleep(1)

        # Clicar no botão de entrar (pode ser o mesmo botão submit)
        botao_entrar = self.wait.until(
            CondicaoExperada.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
        )
        botao_entrar.click()

        # Esperar e clicar no botão Continuar, se aparecer
        try:
            botao_continuar = self.wait.until(
                CondicaoExperada.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Continuar")]'))
            )
            botao_continuar.click()
            print("Botão 'Continuar' clicado.")
        except Exception as e:
            print("Botão 'Continuar' não encontrado ou não necessário.")

    def LogarComFacebook(self):
        print("logando no facebook")
        botao_logar_com_facebook = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (By.XPATH, '//a[text()="Entrar com o Facebook"]')
            )
        )
        botao_logar_com_facebook.click()
        self.InserirDadosLoginFacebook()

    def InserirDadosLoginFacebook(self):
        campo_email = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH,'//input[@name="email"]')))
        campo_senha = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH,'//input[@name="pass"]')))
        botao_login = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH,'//button[@name="login"]')))

        campo_email.clear()
        self.digite_como_uma_pessoa(self.email, campo_email)
        time.sleep(random.randint(1, 3))
        campo_senha.clear()
        self.digite_como_uma_pessoa(self.senha, campo_senha)
        time.sleep(random.randint(1, 3))
        botao_login.click()
        time.sleep(random.randint(4, 7))

    def GerarPlaylist(self):
        lists_dos_artistas = self.ObterLinksDosArtistas()
        for link_do_artista in lists_dos_artistas:
            self.NavegarParaAlbumAtual(link_do_artista)
            self.ObterLinksDosAlbunsDesteArtista()
            self.NavegarParaCadaAlbumDesteArtista(self.links_dos_albuns)
        self.driver.quit()

    def NavegarParaAlbumAtual(self, link_do_artista):
        time.sleep(random.randint(2, 4))
        self.driver.get(link_do_artista)
        self.wait.until(
            CondicaoExperada.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Álbuns"]')
            )
        )
        time.sleep(random.randint(2, 3))


    def NavegarParaCadaAlbumDesteArtista(self, links_do_album):
        for link_album in links_do_album:
                try:
                    self.driver.get(link_album)
                    print('adicionando album: '+ link_album)
                    time.sleep(1)
                    self.AddAlbumParaPlaylist(link_album)
                except:
                    print('não foram encontrados albuns para este artista')
                    pass

    def ClicarNoMenuOpcoesDoAlbum(self):
        try:
            self.actions = ActionChains(self.driver)
            self.wait.until(
                CondicaoExperada.element_to_be_clickable(
                    (By.XPATH, '//button[@class="btn btn-transparent btn--narrow"]')
                )
            )
            menu_opcoes_do_album = self.driver.find_elements(By.XPATH,
                '//button[@class="btn btn-transparent btn--narrow"]'
            )
            time.sleep(random.randint(1, 2))
            self.actions.context_click(menu_opcoes_do_album[1]).perform()
        except:
            pass

    def AddAlbumParaPlaylist(self, album_link):
        self.driver.get(album_link)
        self.ClicarNoMenuOpcoesDoAlbum()
        self.ClicarEmAdicionarParaPlaylist()
        self.ClicarNaPlaylistASerAdicionada(album_link)

    def DescerPagina(self, elemento_referencia, quantidade_de_descidas):
        for descida in range(1, quantidade_de_descidas):
            time.sleep(random.randint(1, 3))
            elemento_referencia.send_keys(Keys.PAGE_DOWN)
            time.sleep(random.randint(1, 3))

    def ClicarNaPlaylistASerAdicionada(self, album_link):
        time.sleep(random.randint(3, 4))
        thumbnail_playlist = self.wait.until(
            CondicaoExperada.visibility_of_any_elements_located(
                (By.XPATH, '//div[@class="mo-coverArt-hoverContainer"]')
            )
        )
        time.sleep(random.randint(4, 6))
        thumbnail_playlist[0].click()
        print('Clicando em "Adicionar a Playlist"')
        time.sleep(random.randint(2, 4))

    def ClicarEmAdicionarParaPlaylist(self):
        add_to_playlist_button = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (
                    By.XPATH,
                    '//nav[@class="react-contextmenu react-contextmenu--visible"]/div[@class="react-contextmenu-item" and text()="Adicionar à playlist"]',
                )
            )
        )
        time.sleep(random.randint(1, 2))
        add_to_playlist_button.click()

    def ObterLinksDosArtistas(self):
        print("Encontrando artistas para este perfíl")
        self.driver.get("https://open.spotify.com/collection/artists")
        first_artist_element = self.wait.until(
            CondicaoExperada.visibility_of_element_located(
                (By.XPATH, '//*[text()="808"]')
            )
        )
        self.DescerPagina(first_artist_element, 10)
        time.sleep(3)
        somentes_hrefs = []
        somente_links_de_artistas = []
        todos_links_na_pagina = self.driver.find_elements(By.TAG_NAME, 'a')
        for elemento in todos_links_na_pagina:
            somentes_hrefs.append(elemento.get_attribute("href"))
    
        for link in somentes_hrefs:
            try:
                if link.index('/artist/') != -1:
                    somente_links_de_artistas.append(link)
            except:
                pass
        return list(dict.fromkeys(somente_links_de_artistas))

    def CarregarMaisAlbuns(self):
        try:
            self.botao_carregar_mais_albuns = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (By.XPATH, '//section[@class=" artist-albums"]//*[text()="MOSTRAR MAIS"]')
            )
            )
            self.botao_carregar_mais_albuns.click()
            time.sleep(random.randint(1, 2))
            self.botao_carregar_mais_albuns = None
            self.botao_carregar_mais_albuns = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (By.XPATH, '//section[@class=" artist-albums"]//*[text()="MOSTRAR MAIS"]')
            )
            )
            if self.botao_carregar_mais_albuns is not None:
                self.botao_carregar_mais_albuns.click()
                print("Carregando mais albuns")
                self.CarregarMaisAlbuns()
        except:
            print("Todos albuns foram carregados")
            pass
        

    def ObterLinksDosAlbunsDesteArtista(self):
        somente_hrefs = []
        links_dos_albuns = []
        links_unicos_dos_albuns = []

        try:
            self.CarregarMaisAlbuns()
        except:
            print("Carregado todos albuns desta página")
            pass

        elemento_secao_album = self.driver.find_elements(By.XPATH, '//section[@class=" artist-albums"]//a')
        for elemento in elemento_secao_album:
            somente_hrefs.append(elemento.get_attribute("href"))

        for link in somente_hrefs:
            try:
                if link.index("/album/") != -1:
                    links_dos_albuns.append(link)
            except:
                pass

        for link in links_dos_albuns:
            links_unicos_dos_albuns.append(link)
        self.links_dos_albuns = list(dict.fromkeys(links_unicos_dos_albuns))

    @staticmethod
    def digite_como_uma_pessoa(frase, campo_input_unico):
        print("Digitando...")
        for letra in frase:
            campo_input_unico.send_keys(letra)
            time.sleep(random.randint(1, 5) / 30)


bot = PlaylistUltimato()
bot.Start()

input("Pressione Enter para fechar o navegador...")