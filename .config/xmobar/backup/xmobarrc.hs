{-# LANGUAGE PostfixOperators    #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE LambdaCase          #-}

{-
   __   __                _
   \ \ / /               | |
    \ V / _ __ ___   ___ | |__   __ _ _ __
    /   \| '_ ` _ \ / _ \| '_ \ / _` | '__|
   / /^\ \ | | | | | (_) | |_) | (_| | |
   \/   \/_| |_| |_|\___/|_.__/ \__,_|_|

Available at: https://gitlab.com/slotThe/dotfiles
Tested and working with GHC 8.10.4 and xmobar git.

Sources of great inspiration have been:
  - https://wiki.archlinux.org/index.php/Xmobar
  - https://gitlab.com/jaor/xmobar-config/

First Edit: 22sep2019 +slot+

GLHF
-}

import Private (email1, email2, email3, stationID)
import Xmobar

import System.Environment (getArgs)

{---------------------------------MAIN----------------------------------}

-- | Execute xmobar with the config.
main :: IO ()
main = getArgs >>= \case
  ["-x", n] -> xmobar . config $ read n
  _         -> xmobar . config $      0

{--------------------------------CONFIG---------------------------------}

-- | The configuration.
config :: Int -> Config
config n = defaultConfig
  { -- Colors
    bgColor = colorBg
  , fgColor = colorFg

  , position = OnScreen n Top

    -- Fonts
  , font            = mainFont
  , additionalFonts = [iconFont, altIconFont]
  , textOffsets     = [11]    -- Offsets for additional fonts (in order).

    -- General behaviour
  , overrideRedirect = False  -- Set the Override Redirect flag (Xlib).
  , commands = myCommands n
  , template = "%" <> screenLog <> "% }{"
            <> "%mail%"
            <> concatMap inSquareBrackets
             [ "%alsa:default:Master%"
             , "%" <> stationID <> "%"
             , "%coretemp%"
             , "%wlp3s0wi%"
             , "%disku%"
             , "%battery%"
             , "%date%"
             ]
  }
 where
  screenLog :: String = "_XMONAD_LOG_" <> show n

  inSquareBrackets :: String -> String
    = wrap (xmobarColor "#808080" "" "[") (xmobarColor "#808080" "" "]")

-- | Commands that I want displayed in my bar.
myCommands :: Int -> [Runnable]
myCommands n =
  [ -- Displays any text received by xmobar on the @_XMONAD_LOG@
    -- property; also strips actions from the text received.
    Run $ XPropertyLog ("_XMONAD_LOG_" <> show n)

  , Run $ Battery
      [ "--template", "<acstatus>"
      , "--Low"     , "15"       -- Low  threshold for colours (in %)
      , "--High"    , "70"       -- High threshold for colours (in %)
      , "--low"     , colorRed
      , "--normal"  , colorFg
      , "--high"    , colorGreen
      , "--suffix"  , "True"     -- Display '%' after '<left>'.
      , "--"                     -- battery specific options start here.
      , "--off"     , "<left> (<timeleft>)"                         -- AC off.
      , "--on"      , yellow "Charging" <> ": <left> (<timeleft>)"  -- AC on.
      , "--idle"    , green  "Charged"  <> " <left>"                -- Fully charged.
        -- Charge strings.  These go _in front_ of the @AC off@ string,
        -- while the @AC on@ and @idle@ strings ignore them.
      , "--lowt"    , "15"       -- Low  threshold for charge strings (in %).
      , "--hight"   , "70"       -- High threshold for charge strings (in %).
      , "--lows"    , inIconFont "\62020  "
      , "--mediums" , inIconFont "\62018  "
      , "--highs"   , inIconFont "\62016  "
      ] (10 `seconds`)

    -- Get station ID from: https://www.wunderground.com/about/faq/international_cities.asp
    -- 23dec2019 +slot+ <weather>
  , Run $ WeatherX stationID
      [ (""                      , inAltIconFont "🌑")
      , ("clear"                 , inAltIconFont "🌣")
      , ("sunny"                 , inAltIconFont "🌣")
      , ("mostly clear"          , inAltIconFont "🌤")
      , ("mostly sunny"          , inAltIconFont "🌤")
      , ("partly sunny"          , inAltIconFont "⛅")
      , ("fair"                  , inAltIconFont "🌑")
      , ("cloudy"                , inAltIconFont "☁")
      , ("overcast"              , inAltIconFont "☁")
      , ("partly cloudy"         , inAltIconFont "⛅")
      , ("mostly cloudy"         , inAltIconFont "🌧")
      , ("considerable cloudines", inAltIconFont "☔")
      ]
      [ "--template", "<skyConditionS> <tempC>°C"
      ] (30 `minutes`)

  , Run $ CoreTemp
      [ "--template", "Tea: <core0>°C  <core1>°C"
      , "--Low"     , "45"      -- unit: °C
      , "--High"    , "65"      -- unit: °C
      , "--low"     , colorFg
      , "--normal"  , colorFg
      , "--high"    , colorRed
      ] (10 `seconds`)

    -- Le current year.
  , Run $ Date ("%a %Y-%m-%d " <> cyan "%H:%M") "date" (10 `seconds`)

    -- Volume with an event based refresh (via alsactl).
    -- 08dec2019 +slot+ event based
  , Run $ Alsa "default" "Master"
      [ "--template", "<volumestatus>"
      , "--suffix"  , "True"  -- Show "%" at the end of the <volume> string.
      , "--"                  -- Volume specific options.
      , "--on"     , ""
      , "--off"    , inAltIconFont "🔇"
      , "--lowv"   , "20"                   -- Low  threshold for strings (in %).
      , "--highv"  , "60"                   -- High threshold for strings (in %).
      , "--lows"   , inIconFont "\61478  "  -- Low    charge string: 
      , "--mediums", inIconFont "\61479  "  -- Medium charge string: 
      , "--highs"  , inIconFont "\61480  "  -- High   charge string: 
      , "--onc"    , colorFg                -- On  colour.
      , "--offc"   , colorFg                -- Off colour.
      ]

  , Run $ DiskU [("/", "ROOT: <used>/<size>")] [] (10 `minutes`)

  , Run $ Wireless "wlp3s0"
      [ "--template", "<essid> <quality>"
      , "--suffix"  , "True"  -- Display '%' after '<quality>'.
      , "--Low"     , "40"
      , "--High"    , "70"
      , "--low"     , colorRed
      , "--normal"  , colorYellow
      , "--high"    , colorGreen
      ] (10 `seconds`)

  , Run $ NotmuchMail "mail"
      [ -- Normal mail addresses
        MailItem "uni:" email1 "not tag:bs"
      , MailItem "mb:"  email2 ""
      , MailItem "mbs:" email3 "not tag:lists and not tag:haskell and not tag:haskell-discourse"

        -- Mailing Lists
      , MailItem "C:"  "" "subject:[Haskell-Cafe]"
      , MailItem "H:"  "" "tag:haskell and not tag:lists"
      , MailItem "L:"  "" "tag:lists"
      , MailItem "bs:" "" "tag:bs"
      , MailItem "hd:" "" "tag:haskell-discourse"
      ] (5 `minutes`)
  ]
 where
  -- | Convenience functions.
  seconds, minutes :: Int -> Int
  seconds = (* 10)
  minutes = (60 *) . seconds

{--------------------------------COLOURS---------------------------------
Unless stated otherwise, all colours are from the "Dracula" colour
scheme.
------------------------------------------------------------------------}

colorBg, colorCyan, colorFg, colorGreen, colorRed, colorYellow :: String
colorRed    = "#ff5555"
colorFg     = "#f8f8f2"
colorBg     = "#5f5f5f" -- Zenburn bg +2
colorGreen  = "#50fa7b"
colorYellow = "#f1fa8c"
colorCyan   = "#8be9fd"

cyan, green, yellow :: String -> String
green  = xmobarColor colorGreen   ""
yellow = xmobarColor colorYellow  ""
cyan   = xmobarColor colorCyan    ""

{- | Use xmobar escape codes to output a string with given foreground and
background colors.

Source: https://hackage.haskell.org/package/xmonad-contrib-0.15/docs/src/XMonad.Hooks.DynamicLog.html#xmobarColor
-}
xmobarColor
  :: String  -- ^ foreground color: a color name, or #rrggbb format
  -> String  -- ^ background color
  -> String  -- ^ output string
  -> String
xmobarColor fg bg = wrap open "</fc>"
 where
  open :: String = concat ["<fc=", fg, if null bg then "" else "," <> bg, ">"]

-- | Wrap a string in delimiters, unless it is empty.
-- Source: https://hackage.haskell.org/package/xmonad-contrib-0.15/docs/src/XMonad.Hooks.DynamicLog.html#wrap
wrap
  :: String  -- ^ left delimiter
  -> String  -- ^ right delimiter
  -> String  -- ^ output string
  -> String
wrap _ _ "" = ""
wrap l r m  = l <> m <> r

{---------------------------------FONTS---------------------------------}

mainFont :: String
mainFont = "xft:scientifica:bold:antialias=false:hinting:false:size=8"

iconFont :: String
iconFont = "xft:FontAwesome-9"

altIconFont :: String
altIconFont = "xft:Symbola-9"

-- | Wrap stuff so it uses the icon font.
inIconFont :: String -> String
inIconFont = wrap "<fn=1>" "</fn>"

-- | Wrap stuff so it uses the alt icon font.
inAltIconFont :: String -> String
inAltIconFont = wrap "<fn=2>" "</fn>"

