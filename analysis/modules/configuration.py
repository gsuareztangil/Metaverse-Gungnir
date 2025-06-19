path_binaries = 'resources\\lib\\'
libunity_path = path_binaries + '++--++\\libunity.so'
libUE4_path = path_binaries + '++--++\\libUE4.so'
path_sources = 'sources\\'
full_project_path = '' # This should be filled in
data_path = '.\\Data\\'

tlds = ["com", "org", "net", "edu", "gov", "io", "me", "tv", "ac", "ad", "ae", "af", "ag", "ai", "al", "am", "ao", "ar", "as", "at", "au", "aw", "ax", "az", "ba", "bb", "bd", "be", "bf", "bg", "bh", "bi", "bj", 
        "bm", "bn", "bo", "br", "bs", "bt", "bv", "bw", "by", "bz", "ca", "cc", "cd", "cf", "cg", "ch", "ci", "ck", "cl", "cm", "cn", "co", "cr", "cu", "cv", "cw", "cx", "cy", "cz", "de", "dj", "dk", "dm", "do", 
        "dz", "ec", "ee", "eg", "eh", "es", "et", "fi", "fj", "fm", "fo", "fr", "ga", "gb", "gd", "ge", "gf", "gg", "gh", "gi", "gl", "gm", "gn", "gp", "gq", "gr", "gt", "gu", "gw", "gy", "hk", "hm", "hn", "hr",
        "ht", "hu", "id", "ie", "il", "im", "in", "io", "iq", "ir", "is", "it", "je", "jm", "jo", "jp", "ke", "kg", "kh", "ki", "km", "kn", "kp", "kr", "kw", "ky", "kz", "la", "lb", "lc", "li", "lk", "lr", "ls",
        "lt", "lu", "lv", "ly", "ma", "mc", "md", "me", "mf", "mg", "mh", "mk", "ml", "mm", "mn", "mo", "mp", "mq", "mr", "ms", "mt", "mu", "mv", "mw", "mx", "my", "mz", "na", "nc", "ne", "nf", "ng", "ni", "nl",
        "no", "np", "nr", "nu", "nz", "om", "pa", "pe", "pf", "pg", "ph", "pk", "pl", "pm", "pn", "pr", "pt", "pw", "py", "qa", "re", "ro", "rs", "ru", "rw", "sa", "sb", "sc", "sd", "se", "sg", "sh", "si", "sj",
        "sk", "sl", "sm", "sn", "so", "sr", "ss", "st", "sv", "sx", "sy", "sz", "tc", "td", "tf", "tg", "th", "tj", "tk", "tl", "tm", "tn", "to", "tr", "tt", "tv", "tz", "ua", "ug", "us", "uy", "uz", "va", "vc",
        "ve", "vg", "vi", "vn", "vu", "wf", "ws", "ye", "yt", "za", "zm", "zw", "aero", "asia", "cat", "coop", "info", "jobs", "museum", "name", "pro", "tel", "post", "test", "dev"]

owners = ["android", "androidx", "com/google", "com/facebook", "com/microsoft", "com/amazon", "com/apple", "org/apache", "org/jetbrains", "com/squareup", "io/reactivex", "com/twitter", "io/flutter", "com/airbnb",
          "com/linkedin", "com/github", "com/ibm", "com/oracle", "com/salesforce", "com/paypal", "com/stripe", "com/adobe", "com/tencent", "com/alibaba", "com/ibm", "org/mongodb", "org/springframework", "io/sentry",
          "com/github/bumptech", "com/squareup/okhttp", "com/jakewharton", "io/realm", "com/uber", "com/vuplex", "com/onesignal", "com/mixpanel", "com/instabug", "com/crashlytics", "com/pusher", "org/greenrobot",
          "org/jsoup", "io/fabric", "com/sendbird", "com/twilio", "com/skype", "com/dropbox", "com/box", "com/samsung", "com/huawei", "com/baidu", "com/yandex", "io/github", "org/conscrypt", "com/stripe", "org/eclipse",
          "com/parse", "com/pinterest", "com/nvidia", "io/agora", "io/swagger", "com/firebase", "com/bitmovin", "com/twitch", "com/spotify", "com/intuit", "com/openai", "com/tesla", "com/adcolony", "com/ironsource",
          "com/chartboost", "com/tapjoy", "com/unity3d", "org/lwjgl", "com/cocos2d", "com/coronalabs", "io/exoplayer", "com/mapbox", "com/tomtom", "com/here", "com/clevertap", "com/branch", "io/applovin", "com/flurry",
          "com/appsflyer", "com/adjust", "com/swrve", "com/kakao", "com/linecorp", "bitter"]

native_owners = ['unity', 'android', 'oculus', 'google','java','kotlin','system','meta','oculus'] #'java','kotlin'