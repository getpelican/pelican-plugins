from pelican import signals
from pelican import contents
import os
import shutil

used_emojis = {}

dict = {
        ':100:': '100.png',
        ':1234:': '1234.png',
        ':-1:': '-1.png',
        ':+1:': '+1.png',
        ':8ball:': '8ball.png',
        ':abcd:': 'abcd.png',
        ':abc:': 'abc.png',
        ':ab:': 'ab.png',
        ':accept:': 'accept.png',
        ':aerial_tramway:': 'aerial_tramway.png',
        ':airplane:': 'airplane.png',
        ':alarm_clock:': 'alarm_clock.png',
        ':alien:': 'alien.png',
        ':ambulance:': 'ambulance.png',
        ':anchor:': 'anchor.png',
        ':angel:': 'angel.png',
        ':anger:': 'anger.png',
        ':angry:': 'angry.png',
        ':anguished:': 'anguished.png',
        ':ant:': 'ant.png',
        ':a:': 'a.png',
        ':apple:': 'apple.png',
        ':aquarius:': 'aquarius.png',
        ':aries:': 'aries.png',
        ':arrow_backward:': 'arrow_backward.png',
        ':arrow_double_down:': 'arrow_double_down.png',
        ':arrow_double_up:': 'arrow_double_up.png',
        ':arrow_down:': 'arrow_down.png',
        ':arrow_down_small:': 'arrow_down_small.png',
        ':arrow_forward:': 'arrow_forward.png',
        ':arrow_heading_down:': 'arrow_heading_down.png',
        ':arrow_heading_up:': 'arrow_heading_up.png',
        ':arrow_left:': 'arrow_left.png',
        ':arrow_lower_left:': 'arrow_lower_left.png',
        ':arrow_lower_right:': 'arrow_lower_right.png',
        ':arrow_right_hook:': 'arrow_right_hook.png',
        ':arrow_right:': 'arrow_right.png',
        ':arrows_clockwise:': 'arrows_clockwise.png',
        ':arrows_counterclockwise:': 'arrows_counterclockwise.png',
        ':arrow_up_down:': 'arrow_up_down.png',
        ':arrow_upper_left:': 'arrow_upper_left.png',
        ':arrow_upper_right:': 'arrow_upper_right.png',
        ':arrow_up:': 'arrow_up.png',
        ':arrow_up_small:': 'arrow_up_small.png',
        ':articulated_lorry:': 'articulated_lorry.png',
        ':art:': 'art.png',
        ':astonished:': 'astonished.png',
        ':atm:': 'atm.png',
        ':baby_bottle:': 'baby_bottle.png',
        ':baby_chick:': 'baby_chick.png',
        ':baby:': 'baby.png',
        ':baby_symbol:': 'baby_symbol.png',
        ':back:': 'back.png',
        ':baggage_claim:': 'baggage_claim.png',
        ':balloon:': 'balloon.png',
        ':ballot_box_with_check:': 'ballot_box_with_check.png',
        ':bamboo:': 'bamboo.png',
        ':banana:': 'banana.png',
        ':bangbang:': 'bangbang.png',
        ':bank:': 'bank.png',
        ':barber:': 'barber.png',
        ':bar_chart:': 'bar_chart.png',
        ':baseball:': 'baseball.png',
        ':basketball:': 'basketball.png',
        ':bath:': 'bath.png',
        ':bathtub:': 'bathtub.png',
        ':battery:': 'battery.png',
        ':bear:': 'bear.png',
        ':bee:': 'bee.png',
        ':beer:': 'beer.png',
        ':beers:': 'beers.png',
        ':beetle:': 'beetle.png',
        ':beginner:': 'beginner.png',
        ':bell:': 'bell.png',
        ':bento:': 'bento.png',
        ':bicyclist:': 'bicyclist.png',
        ':bike:': 'bike.png',
        ':bikini:': 'bikini.png',
        ':bird:': 'bird.png',
        ':birthday:': 'birthday.png',
        ':black_circle:': 'black_circle.png',
        ':black_joker:': 'black_joker.png',
        ':black_medium_small_square:': 'black_medium_small_square.png',
        ':black_medium_square:': 'black_medium_square.png',
        ':black_nib:': 'black_nib.png',
        ':black_small_square:': 'black_small_square.png',
        ':black_square_button:': 'black_square_button.png',
        ':black_square:': 'black_square.png',
        ':blossom:': 'blossom.png',
        ':blowfish:': 'blowfish.png',
        ':blue_book:': 'blue_book.png',
        ':blue_car:': 'blue_car.png',
        ':blue_heart:': 'blue_heart.png',
        ':blush:': 'blush.png',
        ':boar:': 'boar.png',
        ':boat:': 'boat.png',
        ':bomb:': 'bomb.png',
        ':bookmark:': 'bookmark.png',
        ':bookmark_tabs:': 'bookmark_tabs.png',
        ':book:': 'book.png',
        ':books:': 'books.png',
        ':boom:': 'boom.png',
        ':boot:': 'boot.png',
        ':bouquet:': 'bouquet.png',
        ':bowling:': 'bowling.png',
        ':bow:': 'bow.png',
        ':bowtie:': 'bowtie.png',
        ':boy:': 'boy.png',
        ':b:': 'b.png',
        ':bread:': 'bread.png',
        ':bride_with_veil:': 'bride_with_veil.png',
        ':bridge_at_night:': 'bridge_at_night.png',
        ':briefcase:': 'briefcase.png',
        ':broken_heart:': 'broken_heart.png',
        ':bug:': 'bug.png',
        ':bulb:': 'bulb.png',
        ':bullettrain_front:': 'bullettrain_front.png',
        ':bullettrain_side:': 'bullettrain_side.png',
        ':bus:': 'bus.png',
        ':busstop:': 'busstop.png',
        ':bust_in_silhouette:': 'bust_in_silhouette.png',
        ':busts_in_silhouette:': 'busts_in_silhouette.png',
        ':cactus:': 'cactus.png',
        ':cake:': 'cake.png',
        ':calendar:': 'calendar.png',
        ':calling:': 'calling.png',
        ':camel:': 'camel.png',
        ':camera:': 'camera.png',
        ':cancer:': 'cancer.png',
        ':candy:': 'candy.png',
        ':capital_abcd:': 'capital_abcd.png',
        ':capricorn:': 'capricorn.png',
        ':card_index:': 'card_index.png',
        ':carousel_horse:': 'carousel_horse.png',
        ':car:': 'car.png',
        ':cat2:': 'cat2.png',
        ':cat:': 'cat.png',
        ':cd:': 'cd.png',
        ':chart:': 'chart.png',
        ':chart_with_downwards_trend:': 'chart_with_downwards_trend.png',
        ':chart_with_upwards_trend:': 'chart_with_upwards_trend.png',
        ':checkered_flag:': 'checkered_flag.png',
        ':cherries:': 'cherries.png',
        ':cherry_blossom:': 'cherry_blossom.png',
        ':chestnut:': 'chestnut.png',
        ':chicken:': 'chicken.png',
        ':children_crossing:': 'children_crossing.png',
        ':chocolate_bar:': 'chocolate_bar.png',
        ':christmas_tree:': 'christmas_tree.png',
        ':church:': 'church.png',
        ':cinema:': 'cinema.png',
        ':circus_tent:': 'circus_tent.png',
        ':city_sunrise:': 'city_sunrise.png',
        ':city_sunset:': 'city_sunset.png',
        ':clapper:': 'clapper.png',
        ':clap:': 'clap.png',
        ':clipboard:': 'clipboard.png',
        ':clock1030:': 'clock1030.png',
        ':clock10:': 'clock10.png',
        ':clock1130:': 'clock1130.png',
        ':clock11:': 'clock11.png',
        ':clock1230:': 'clock1230.png',
        ':clock12:': 'clock12.png',
        ':clock130:': 'clock130.png',
        ':clock1:': 'clock1.png',
        ':clock230:': 'clock230.png',
        ':clock2:': 'clock2.png',
        ':clock330:': 'clock330.png',
        ':clock3:': 'clock3.png',
        ':clock430:': 'clock430.png',
        ':clock4:': 'clock4.png',
        ':clock530:': 'clock530.png',
        ':clock5:': 'clock5.png',
        ':clock630:': 'clock630.png',
        ':clock6:': 'clock6.png',
        ':clock730:': 'clock730.png',
        ':clock7:': 'clock7.png',
        ':clock830:': 'clock830.png',
        ':clock8:': 'clock8.png',
        ':clock930:': 'clock930.png',
        ':clock9:': 'clock9.png',
        ':closed_book:': 'closed_book.png',
        ':closed_lock_with_key:': 'closed_lock_with_key.png',
        ':closed_umbrella:': 'closed_umbrella.png',
        ':cloud:': 'cloud.png',
        ':cl:': 'cl.png',
        ':clubs:': 'clubs.png',
        ':cn:': 'cn.png',
        ':cocktail:': 'cocktail.png',
        ':coffee:': 'coffee.png',
        ':cold_sweat:': 'cold_sweat.png',
        ':collision:': 'collision.png',
        ':computer:': 'computer.png',
        ':confetti_ball:': 'confetti_ball.png',
        ':confounded:': 'confounded.png',
        ':confused:': 'confused.png',
        ':congratulations:': 'congratulations.png',
        ':construction:': 'construction.png',
        ':construction_worker:': 'construction_worker.png',
        ':convenience_store:': 'convenience_store.png',
        ':cookie:': 'cookie.png',
        ':cool:': 'cool.png',
        ':cop:': 'cop.png',
        ':copyright:': 'copyright.png',
        ':corn:': 'corn.png',
        ':couplekiss:': 'couplekiss.png',
        ':couple:': 'couple.png',
        ':couple_with_heart:': 'couple_with_heart.png',
        ':cow2:': 'cow2.png',
        ':cow:': 'cow.png',
        ':credit_card:': 'credit_card.png',
        ':crescent_moon:': 'crescent_moon.png',
        ':crocodile:': 'crocodile.png',
        ':crossed_flags:': 'crossed_flags.png',
        ':crown:': 'crown.png',
        ':crying_cat_face:': 'crying_cat_face.png',
        ':cry:': 'cry.png',
        ':crystal_ball:': 'crystal_ball.png',
        ':cupid:': 'cupid.png',
        ':curly_loop:': 'curly_loop.png',
        ':currency_exchange:': 'currency_exchange.png',
        ':curry:': 'curry.png',
        ':custard:': 'custard.png',
        ':customs:': 'customs.png',
        ':cyclone:': 'cyclone.png',
        ':dancer:': 'dancer.png',
        ':dancers:': 'dancers.png',
        ':dango:': 'dango.png',
        ':dart:': 'dart.png',
        ':dash:': 'dash.png',
        ':date:': 'date.png',
        ':deciduous_tree:': 'deciduous_tree.png',
        ':department_store:': 'department_store.png',
        ':de:': 'de.png',
        ':diamond_shape_with_a_dot_inside:':
        'diamond_shape_with_a_dot_inside.png',
        ':diamonds:': 'diamonds.png',
        ':disappointed:': 'disappointed.png',
        ':disappointed_relieved:': 'disappointed_relieved.png',
        ':dizzy_face:': 'dizzy_face.png',
        ':dizzy:': 'dizzy.png',
        ':dog2:': 'dog2.png',
        ':dog:': 'dog.png',
        ':dollar:': 'dollar.png',
        ':dolls:': 'dolls.png',
        ':dolphin:': 'dolphin.png',
        ':do_not_litter:': 'do_not_litter.png',
        ':donut:': 'donut.png',
        ':door:': 'door.png',
        ':doughnut:': 'doughnut.png',
        ':dragon_face:': 'dragon_face.png',
        ':dragon:': 'dragon.png',
        ':dress:': 'dress.png',
        ':dromedary_camel:': 'dromedary_camel.png',
        ':droplet:': 'droplet.png',
        ':dvd:': 'dvd.png',
        ':ear_of_rice:': 'ear_of_rice.png',
        ':ear:': 'ear.png',
        ':earth_africa:': 'earth_africa.png',
        ':earth_americas:': 'earth_americas.png',
        ':earth_asia:': 'earth_asia.png',
        ':eggplant:': 'eggplant.png',
        ':egg:': 'egg.png',
        ':eight:': 'eight.png',
        ':eight_pointed_black_star:': 'eight_pointed_black_star.png',
        ':eight_spoked_asterisk:': 'eight_spoked_asterisk.png',
        ':electric_plug:': 'electric_plug.png',
        ':elephant:': 'elephant.png',
        ':e-mail:': 'e-mail.png',
        ':email:': 'email.png',
        ':end:': 'end.png',
        ':envelope:': 'envelope.png',
        ':es:': 'es.png',
        ':european_castle:': 'european_castle.png',
        ':european_post_office:': 'european_post_office.png',
        ':euro:': 'euro.png',
        ':evergreen_tree:': 'evergreen_tree.png',
        ':exclamation:': 'exclamation.png',
        ':expressionless:': 'expressionless.png',
        ':eyeglasses:': 'eyeglasses.png',
        ':eyes:': 'eyes.png',
        ':facepunch:': 'facepunch.png',
        ':factory:': 'factory.png',
        ':fallen_leaf:': 'fallen_leaf.png',
        ':family:': 'family.png',
        ':fast_forward:': 'fast_forward.png',
        ':fax:': 'fax.png',
        ':fearful:': 'fearful.png',
        ':feelsgood:': 'feelsgood.png',
        ':feet:': 'feet.png',
        ':ferris_wheel:': 'ferris_wheel.png',
        ':file_folder:': 'file_folder.png',
        ':finnadie:': 'finnadie.png',
        ':fire_engine:': 'fire_engine.png',
        ':fire:': 'fire.png',
        ':fireworks:': 'fireworks.png',
        ':first_quarter_moon:': 'first_quarter_moon.png',
        ':first_quarter_moon_with_face:': 'first_quarter_moon_with_face.png',
        ':fish_cake:': 'fish_cake.png',
        ':fishing_pole_and_fish:': 'fishing_pole_and_fish.png',
        ':fish:': 'fish.png',
        ':fist:': 'fist.png',
        ':five:': 'five.png',
        ':flags:': 'flags.png',
        ':flashlight:': 'flashlight.png',
        ':floppy_disk:': 'floppy_disk.png',
        ':flower_playing_cards:': 'flower_playing_cards.png',
        ':flushed:': 'flushed.png',
        ':foggy:': 'foggy.png',
        ':football:': 'football.png',
        ':fork_and_knife:': 'fork_and_knife.png',
        ':fountain:': 'fountain.png',
        ':four_leaf_clover:': 'four_leaf_clover.png',
        ':four:': 'four.png',
        ':free:': 'free.png',
        ':fried_shrimp:': 'fried_shrimp.png',
        ':fries:': 'fries.png',
        ':frog:': 'frog.png',
        ':frowning:': 'frowning.png',
        ':fr:': 'fr.png',
        ':fuelpump:': 'fuelpump.png',
        ':full_moon:': 'full_moon.png',
        ':full_moon_with_face:': 'full_moon_with_face.png',
        ':fu:': 'fu.png',
        ':game_die:': 'game_die.png',
        ':gb:': 'gb.png',
        ':gemini:': 'gemini.png',
        ':gem:': 'gem.png',
        ':ghost:': 'ghost.png',
        ':gift_heart:': 'gift_heart.png',
        ':gift:': 'gift.png',
        ':girl:': 'girl.png',
        ':globe_with_meridians:': 'globe_with_meridians.png',
        ':goat:': 'goat.png',
        ':goberserk:': 'goberserk.png',
        ':godmode:': 'godmode.png',
        ':golf:': 'golf.png',
        ':grapes:': 'grapes.png',
        ':green_apple:': 'green_apple.png',
        ':green_book:': 'green_book.png',
        ':green_heart:': 'green_heart.png',
        ':grey_exclamation:': 'grey_exclamation.png',
        ':grey_question:': 'grey_question.png',
        ':grimacing:': 'grimacing.png',
        ':grinning:': 'grinning.png',
        ':grin:': 'grin.png',
        ':guardsman:': 'guardsman.png',
        ':guitar:': 'guitar.png',
        ':gun:': 'gun.png',
        ':haircut:': 'haircut.png',
        ':hamburger:': 'hamburger.png',
        ':hammer:': 'hammer.png',
        ':hamster:': 'hamster.png',
        ':handbag:': 'handbag.png',
        ':hand:': 'hand.png',
        ':hankey:': 'hankey.png',
        ':hash:': 'hash.png',
        ':hatched_chick:': 'hatched_chick.png',
        ':hatching_chick:': 'hatching_chick.png',
        ':headphones:': 'headphones.png',
        ':hear_no_evil:': 'hear_no_evil.png',
        ':heartbeat:': 'heartbeat.png',
        ':heart_decoration:': 'heart_decoration.png',
        ':heart_eyes_cat:': 'heart_eyes_cat.png',
        ':heart_eyes:': 'heart_eyes.png',
        ':heart:': 'heart.png',
        ':heartpulse:': 'heartpulse.png',
        ':hearts:': 'hearts.png',
        ':heavy_check_mark:': 'heavy_check_mark.png',
        ':heavy_division_sign:': 'heavy_division_sign.png',
        ':heavy_dollar_sign:': 'heavy_dollar_sign.png',
        ':heavy_exclamation_mark:': 'heavy_exclamation_mark.png',
        ':heavy_minus_sign:': 'heavy_minus_sign.png',
        ':heavy_multiplication_x:': 'heavy_multiplication_x.png',
        ':heavy_plus_sign:': 'heavy_plus_sign.png',
        ':helicopter:': 'helicopter.png',
        ':herb:': 'herb.png',
        ':hibiscus:': 'hibiscus.png',
        ':high_brightness:': 'high_brightness.png',
        ':high_heel:': 'high_heel.png',
        ':hocho:': 'hocho.png',
        ':honeybee:': 'honeybee.png',
        ':honey_pot:': 'honey_pot.png',
        ':horse:': 'horse.png',
        ':horse_racing:': 'horse_racing.png',
        ':hospital:': 'hospital.png',
        ':hotel:': 'hotel.png',
        ':hotsprings:': 'hotsprings.png',
        ':hourglass_flowing_sand:': 'hourglass_flowing_sand.png',
        ':hourglass:': 'hourglass.png',
        ':house:': 'house.png',
        ':house_with_garden:': 'house_with_garden.png',
        ':hurtrealbad:': 'hurtrealbad.png',
        ':hushed:': 'hushed.png',
        ':ice_cream:': 'ice_cream.png',
        ':icecream:': 'icecream.png',
        ':ideograph_advantage:': 'ideograph_advantage.png',
        ':id:': 'id.png',
        ':imp:': 'imp.png',
        ':inbox_tray:': 'inbox_tray.png',
        ':incoming_envelope:': 'incoming_envelope.png',
        ':information_desk_person:': 'information_desk_person.png',
        ':information_source:': 'information_source.png',
        ':innocent:': 'innocent.png',
        ':interrobang:': 'interrobang.png',
        ':iphone:': 'iphone.png',
        ':it:': 'it.png',
        ':izakaya_lantern:': 'izakaya_lantern.png',
        ':jack_o_lantern:': 'jack_o_lantern.png',
        ':japanese_castle:': 'japanese_castle.png',
        ':japanese_goblin:': 'japanese_goblin.png',
        ':japanese_ogre:': 'japanese_ogre.png',
        ':japan:': 'japan.png',
        ':jeans:': 'jeans.png',
        ':joy_cat:': 'joy_cat.png',
        ':joy:': 'joy.png',
        ':jp:': 'jp.png',
        ':keycap_ten:': 'keycap_ten.png',
        ':key:': 'key.png',
        ':kimono:': 'kimono.png',
        ':kissing_cat:': 'kissing_cat.png',
        ':kissing_closed_eyes:': 'kissing_closed_eyes.png',
        ':kissing_face:': 'kissing_face.png',
        ':kissing_heart:': 'kissing_heart.png',
        ':kissing:': 'kissing.png',
        ':kissing_smiling_eyes:': 'kissing_smiling_eyes.png',
        ':kiss:': 'kiss.png',
        ':koala:': 'koala.png',
        ':koko:': 'koko.png',
        ':kr:': 'kr.png',
        ':large_blue_circle:': 'large_blue_circle.png',
        ':large_blue_diamond:': 'large_blue_diamond.png',
        ':large_orange_diamond:': 'large_orange_diamond.png',
        ':last_quarter_moon:': 'last_quarter_moon.png',
        ':last_quarter_moon_with_face:': 'last_quarter_moon_with_face.png',
        ':laughing:': 'laughing.png',
        ':leaves:': 'leaves.png',
        ':ledger:': 'ledger.png',
        ':left_luggage:': 'left_luggage.png',
        ':left_right_arrow:': 'left_right_arrow.png',
        ':leftwards_arrow_with_hook:': 'leftwards_arrow_with_hook.png',
        ':lemon:': 'lemon.png',
        ':leopard:': 'leopard.png',
        ':leo:': 'leo.png',
        ':libra:': 'libra.png',
        ':light_rail:': 'light_rail.png',
        ':link:': 'link.png',
        ':lips:': 'lips.png',
        ':lipstick:': 'lipstick.png',
        ':lock:': 'lock.png',
        ':lock_with_ink_pen:': 'lock_with_ink_pen.png',
        ':lollipop:': 'lollipop.png',
        ':loop:': 'loop.png',
        ':loudspeaker:': 'loudspeaker.png',
        ':love_hotel:': 'love_hotel.png',
        ':love_letter:': 'love_letter.png',
        ':low_brightness:': 'low_brightness.png',
        ':mag:': 'mag.png',
        ':mag_right:': 'mag_right.png',
        ':mahjong:': 'mahjong.png',
        ':mailbox_closed:': 'mailbox_closed.png',
        ':mailbox:': 'mailbox.png',
        ':mailbox_with_mail:': 'mailbox_with_mail.png',
        ':mailbox_with_no_mail:': 'mailbox_with_no_mail.png',
        ':man:': 'man.png',
        ':mans_shoe:': 'mans_shoe.png',
        ':man_with_gua_pi_mao:': 'man_with_gua_pi_mao.png',
        ':man_with_turban:': 'man_with_turban.png',
        ':maple_leaf:': 'maple_leaf.png',
        ':mask:': 'mask.png',
        ':massage:': 'massage.png',
        ':meat_on_bone:': 'meat_on_bone.png',
        ':mega:': 'mega.png',
        ':melon:': 'melon.png',
        ':memo:': 'memo.png',
        ':mens:': 'mens.png',
        ':metal:': 'metal.png',
        ':metro:': 'metro.png',
        ':microphone:': 'microphone.png',
        ':microscope:': 'microscope.png',
        ':milky_way:': 'milky_way.png',
        ':minibus:': 'minibus.png',
        ':minidisc:': 'minidisc.png',
        ':mobile_phone_off:': 'mobile_phone_off.png',
        ':moneybag:': 'moneybag.png',
        ':money_with_wings:': 'money_with_wings.png',
        ':monkey_face:': 'monkey_face.png',
        ':monkey:': 'monkey.png',
        ':monorail:': 'monorail.png',
        ':mortar_board:': 'mortar_board.png',
        ':mountain_bicyclist:': 'mountain_bicyclist.png',
        ':mountain_cableway:': 'mountain_cableway.png',
        ':mountain_railway:': 'mountain_railway.png',
        ':mount_fuji:': 'mount_fuji.png',
        ':mouse2:': 'mouse2.png',
        ':mouse:': 'mouse.png',
        ':movie_camera:': 'movie_camera.png',
        ':moyai:': 'moyai.png',
        ':m:': 'm.png',
        ':muscle:': 'muscle.png',
        ':mushroom:': 'mushroom.png',
        ':musical_keyboard:': 'musical_keyboard.png',
        ':musical_note:': 'musical_note.png',
        ':musical_score:': 'musical_score.png',
        ':mute:': 'mute.png',
        ':nail_care:': 'nail_care.png',
        ':name_badge:': 'name_badge.png',
        ':neckbeard:': 'neckbeard.png',
        ':necktie:': 'necktie.png',
        ':negative_squared_cross_mark:': 'negative_squared_cross_mark.png',
        ':neutral_face:': 'neutral_face.png',
        ':new_moon:': 'new_moon.png',
        ':new_moon_with_face:': 'new_moon_with_face.png',
        ':new:': 'new.png',
        ':newspaper:': 'newspaper.png',
        ':ng:': 'ng.png',
        ':nine:': 'nine.png',
        ':no_bell:': 'no_bell.png',
        ':no_bicycles:': 'no_bicycles.png',
        ':no_entry:': 'no_entry.png',
        ':no_entry_sign:': 'no_entry_sign.png',
        ':no_good:': 'no_good.png',
        ':no_mobile_phones:': 'no_mobile_phones.png',
        ':no_mouth:': 'no_mouth.png',
        ':non-potable_water:': 'non-potable_water.png',
        ':no_pedestrians:': 'no_pedestrians.png',
        ':nose:': 'nose.png',
        ':no_smoking:': 'no_smoking.png',
        ':notebook:': 'notebook.png',
        ':notebook_with_decorative_cover:':
        'notebook_with_decorative_cover.png',
        ':notes:': 'notes.png',
        ':nut_and_bolt:': 'nut_and_bolt.png',
        ':o2:': 'o2.png',
        ':ocean:': 'ocean.png',
        ':octocat:': 'octocat.png',
        ':octopus:': 'octopus.png',
        ':oden:': 'oden.png',
        ':office:': 'office.png',
        ':ok_hand:': 'ok_hand.png',
        ':ok:': 'ok.png',
        ':ok_woman:': 'ok_woman.png',
        ':older_man:': 'older_man.png',
        ':older_woman:': 'older_woman.png',
        ':oncoming_automobile:': 'oncoming_automobile.png',
        ':oncoming_bus:': 'oncoming_bus.png',
        ':oncoming_police_car:': 'oncoming_police_car.png',
        ':oncoming_taxi:': 'oncoming_taxi.png',
        ':one:': 'one.png',
        ':on:': 'on.png',
        ':open_file_folder:': 'open_file_folder.png',
        ':open_hands:': 'open_hands.png',
        ':open_mouth:': 'open_mouth.png',
        ':ophiuchus:': 'ophiuchus.png',
        ':o:': 'o.png',
        ':orange_book:': 'orange_book.png',
        ':outbox_tray:': 'outbox_tray.png',
        ':ox:': 'ox.png',
        ':package:': 'package.png',
        ':page_facing_up:': 'page_facing_up.png',
        ':pager:': 'pager.png',
        ':page_with_curl:': 'page_with_curl.png',
        ':palm_tree:': 'palm_tree.png',
        ':panda_face:': 'panda_face.png',
        ':paperclip:': 'paperclip.png',
        ':parking:': 'parking.png',
        ':part_alternation_mark:': 'part_alternation_mark.png',
        ':partly_sunny:': 'partly_sunny.png',
        ':passport_control:': 'passport_control.png',
        ':paw_prints:': 'paw_prints.png',
        ':peach:': 'peach.png',
        ':pear:': 'pear.png',
        ':pencil2:': 'pencil2.png',
        ':pencil:': 'pencil.png',
        ':penguin:': 'penguin.png',
        ':pensive:': 'pensive.png',
        ':performing_arts:': 'performing_arts.png',
        ':persevere:': 'persevere.png',
        ':person_frowning:': 'person_frowning.png',
        ':person_with_blond_hair:': 'person_with_blond_hair.png',
        ':person_with_pouting_face:': 'person_with_pouting_face.png',
        ':phone:': 'phone.png',
        ':pig2:': 'pig2.png',
        ':pig_nose:': 'pig_nose.png',
        ':pig:': 'pig.png',
        ':pill:': 'pill.png',
        ':pineapple:': 'pineapple.png',
        ':pisces:': 'pisces.png',
        ':pizza:': 'pizza.png',
        ':plus1:': 'plus1.png',
        ':point_down:': 'point_down.png',
        ':point_left:': 'point_left.png',
        ':point_right:': 'point_right.png',
        ':point_up_2:': 'point_up_2.png',
        ':point_up:': 'point_up.png',
        ':police_car:': 'police_car.png',
        ':poodle:': 'poodle.png',
        ':poop:': 'poop.png',
        ':postal_horn:': 'postal_horn.png',
        ':postbox:': 'postbox.png',
        ':post_office:': 'post_office.png',
        ':potable_water:': 'potable_water.png',
        ':pouch:': 'pouch.png',
        ':poultry_leg:': 'poultry_leg.png',
        ':pound:': 'pound.png',
        ':pouting_cat:': 'pouting_cat.png',
        ':pray:': 'pray.png',
        ':princess:': 'princess.png',
        ':punch:': 'punch.png',
        ':purple_heart:': 'purple_heart.png',
        ':purse:': 'purse.png',
        ':pushpin:': 'pushpin.png',
        ':put_litter_in_its_place:': 'put_litter_in_its_place.png',
        ':question:': 'question.png',
        ':rabbit2:': 'rabbit2.png',
        ':rabbit:': 'rabbit.png',
        ':racehorse:': 'racehorse.png',
        ':radio_button:': 'radio_button.png',
        ':radio:': 'radio.png',
        ':rage1:': 'rage1.png',
        ':rage2:': 'rage2.png',
        ':rage3:': 'rage3.png',
        ':rage4:': 'rage4.png',
        ':rage:': 'rage.png',
        ':railway_car:': 'railway_car.png',
        ':rainbow:': 'rainbow.png',
        ':raised_hand:': 'raised_hand.png',
        ':raised_hands:': 'raised_hands.png',
        ':raising_hand:': 'raising_hand.png',
        ':ramen:': 'ramen.png',
        ':ram:': 'ram.png',
        ':rat:': 'rat.png',
        ':recycle:': 'recycle.png',
        ':red_car:': 'red_car.png',
        ':red_circle:': 'red_circle.png',
        ':registered:': 'registered.png',
        ':relaxed:': 'relaxed.png',
        ':relieved:': 'relieved.png',
        ':repeat_one:': 'repeat_one.png',
        ':repeat:': 'repeat.png',
        ':restroom:': 'restroom.png',
        ':revolving_hearts:': 'revolving_hearts.png',
        ':rewind:': 'rewind.png',
        ':ribbon:': 'ribbon.png',
        ':rice_ball:': 'rice_ball.png',
        ':rice_cracker:': 'rice_cracker.png',
        ':rice:': 'rice.png',
        ':rice_scene:': 'rice_scene.png',
        ':ring:': 'ring.png',
        ':rocket:': 'rocket.png',
        ':roller_coaster:': 'roller_coaster.png',
        ':rooster:': 'rooster.png',
        ':rose:': 'rose.png',
        ':rotating_light:': 'rotating_light.png',
        ':round_pushpin:': 'round_pushpin.png',
        ':rowboat:': 'rowboat.png',
        ':rugby_football:': 'rugby_football.png',
        ':runner:': 'runner.png',
        ':running:': 'running.png',
        ':running_shirt_with_sash:': 'running_shirt_with_sash.png',
        ':ru:': 'ru.png',
        ':sagittarius:': 'sagittarius.png',
        ':sailboat:': 'sailboat.png',
        ':sake:': 'sake.png',
        ':sandal:': 'sandal.png',
        ':santa:': 'santa.png',
        ':sa:': 'sa.png',
        ':satellite:': 'satellite.png',
        ':satisfied:': 'satisfied.png',
        ':saxophone:': 'saxophone.png',
        ':school:': 'school.png',
        ':school_satchel:': 'school_satchel.png',
        ':scissors:': 'scissors.png',
        ':scorpius:': 'scorpius.png',
        ':scream_cat:': 'scream_cat.png',
        ':scream:': 'scream.png',
        ':scroll:': 'scroll.png',
        ':seat:': 'seat.png',
        ':secret:': 'secret.png',
        ':seedling:': 'seedling.png',
        ':see_no_evil:': 'see_no_evil.png',
        ':seven:': 'seven.png',
        ':shaved_ice:': 'shaved_ice.png',
        ':sheep:': 'sheep.png',
        ':shell:': 'shell.png',
        ':shipit:': 'shipit.png',
        ':ship:': 'ship.png',
        ':shirt:': 'shirt.png',
        ':shit:': 'shit.png',
        ':shoe:': 'shoe.png',
        ':shower:': 'shower.png',
        ':signal_strength:': 'signal_strength.png',
        ':six:': 'six.png',
        ':six_pointed_star:': 'six_pointed_star.png',
        ':ski:': 'ski.png',
        ':skull:': 'skull.png',
        ':sleeping:': 'sleeping.png',
        ':sleepy:': 'sleepy.png',
        ':slot_machine:': 'slot_machine.png',
        ':small_blue_diamond:': 'small_blue_diamond.png',
        ':small_orange_diamond:': 'small_orange_diamond.png',
        ':small_red_triangle_down:': 'small_red_triangle_down.png',
        ':small_red_triangle:': 'small_red_triangle.png',
        ':smile_cat:': 'smile_cat.png',
        ':smile:': 'smile.png',
        ':smiley_cat:': 'smiley_cat.png',
        ':smiley:': 'smiley.png',
        ':smiling_imp:': 'smiling_imp.png',
        ':smirk_cat:': 'smirk_cat.png',
        ':smirk:': 'smirk.png',
        ':smoking:': 'smoking.png',
        ':snail:': 'snail.png',
        ':snake:': 'snake.png',
        ':snowboarder:': 'snowboarder.png',
        ':snowflake:': 'snowflake.png',
        ':snowman:': 'snowman.png',
        ':sob:': 'sob.png',
        ':soccer:': 'soccer.png',
        ':soon:': 'soon.png',
        ':sos:': 'sos.png',
        ':sound:': 'sound.png',
        ':space_invader:': 'space_invader.png',
        ':spades:': 'spades.png',
        ':spaghetti:': 'spaghetti.png',
        ':sparkle:': 'sparkle.png',
        ':sparkler:': 'sparkler.png',
        ':sparkles:': 'sparkles.png',
        ':sparkling_heart:': 'sparkling_heart.png',
        ':speaker:': 'speaker.png',
        ':speak_no_evil:': 'speak_no_evil.png',
        ':speech_balloon:': 'speech_balloon.png',
        ':speedboat:': 'speedboat.png',
        ':squirrel:': 'squirrel.png',
        ':star2:': 'star2.png',
        ':star:': 'star.png',
        ':stars:': 'stars.png',
        ':station:': 'station.png',
        ':statue_of_liberty:': 'statue_of_liberty.png',
        ':steam_locomotive:': 'steam_locomotive.png',
        ':stew:': 'stew.png',
        ':straight_ruler:': 'straight_ruler.png',
        ':strawberry:': 'strawberry.png',
        ':stuck_out_tongue_closed_eyes:': 'stuck_out_tongue_closed_eyes.png',
        ':stuck_out_tongue:': 'stuck_out_tongue.png',
        ':stuck_out_tongue_winking_eye:': 'stuck_out_tongue_winking_eye.png',
        ':sunflower:': 'sunflower.png',
        ':sunglasses:': 'sunglasses.png',
        ':sunny:': 'sunny.png',
        ':sunrise_over_mountains:': 'sunrise_over_mountains.png',
        ':sunrise:': 'sunrise.png',
        ':sun_with_face:': 'sun_with_face.png',
        ':surfer:': 'surfer.png',
        ':sushi:': 'sushi.png',
        ':suspect:': 'suspect.png',
        ':suspension_railway:': 'suspension_railway.png',
        ':sweat_drops:': 'sweat_drops.png',
        ':sweat:': 'sweat.png',
        ':sweat_smile:': 'sweat_smile.png',
        ':sweet_potato:': 'sweet_potato.png',
        ':swimmer:': 'swimmer.png',
        ':symbols:': 'symbols.png',
        ':syringe:': 'syringe.png',
        ':tada:': 'tada.png',
        ':tanabata_tree:': 'tanabata_tree.png',
        ':tangerine:': 'tangerine.png',
        ':taurus:': 'taurus.png',
        ':taxi:': 'taxi.png',
        ':tea:': 'tea.png',
        ':telephone:': 'telephone.png',
        ':telephone_receiver:': 'telephone_receiver.png',
        ':telescope:': 'telescope.png',
        ':tennis:': 'tennis.png',
        ':tent:': 'tent.png',
        ':thought_balloon:': 'thought_balloon.png',
        ':three:': 'three.png',
        ':thumbsdown:': 'thumbsdown.png',
        ':thumbsup:': 'thumbsup.png',
        ':ticket:': 'ticket.png',
        ':tiger2:': 'tiger2.png',
        ':tiger:': 'tiger.png',
        ':tired_face:': 'tired_face.png',
        ':tm:': 'tm.png',
        ':toilet:': 'toilet.png',
        ':tokyo_tower:': 'tokyo_tower.png',
        ':tomato:': 'tomato.png',
        ':tongue:': 'tongue.png',
        ':tophat:': 'tophat.png',
        ':top:': 'top.png',
        ':tractor:': 'tractor.png',
        ':traffic_light:': 'traffic_light.png',
        ':train2:': 'train2.png',
        ':train:': 'train.png',
        ':tram:': 'tram.png',
        ':triangular_flag_on_post:': 'triangular_flag_on_post.png',
        ':triangular_ruler:': 'triangular_ruler.png',
        ':trident:': 'trident.png',
        ':triumph:': 'triumph.png',
        ':trolleybus:': 'trolleybus.png',
        ':trollface:': 'trollface.png',
        ':trophy:': 'trophy.png',
        ':tropical_drink:': 'tropical_drink.png',
        ':tropical_fish:': 'tropical_fish.png',
        ':truck:': 'truck.png',
        ':trumpet:': 'trumpet.png',
        ':tshirt:': 'tshirt.png',
        ':tulip:': 'tulip.png',
        ':turtle:': 'turtle.png',
        ':tv:': 'tv.png',
        ':twisted_rightwards_arrows:': 'twisted_rightwards_arrows.png',
        ':two_hearts:': 'two_hearts.png',
        ':two_men_holding_hands:': 'two_men_holding_hands.png',
        ':two:': 'two.png',
        ':two_women_holding_hands:': 'two_women_holding_hands.png',
        ':u5272:': 'u5272.png',
        ':u5408:': 'u5408.png',
        ':u55b6:': 'u55b6.png',
        ':u6307:': 'u6307.png',
        ':u6708:': 'u6708.png',
        ':u6709:': 'u6709.png',
        ':u6e80:': 'u6e80.png',
        ':u7121:': 'u7121.png',
        ':u7533:': 'u7533.png',
        ':u7981:': 'u7981.png',
        ':u7a7a:': 'u7a7a.png',
        ':uk:': 'uk.png',
        ':umbrella:': 'umbrella.png',
        ':unamused:': 'unamused.png',
        ':underage:': 'underage.png',
        ':unlock:': 'unlock.png',
        ':up:': 'up.png',
        ':us:': 'us.png',
        ':vertical_traffic_light:': 'vertical_traffic_light.png',
        ':vhs:': 'vhs.png',
        ':vibration_mode:': 'vibration_mode.png',
        ':video_camera:': 'video_camera.png',
        ':video_game:': 'video_game.png',
        ':violin:': 'violin.png',
        ':virgo:': 'virgo.png',
        ':volcano:': 'volcano.png',
        ':v:': 'v.png',
        ':vs:': 'vs.png',
        ':walking:': 'walking.png',
        ':waning_crescent_moon:': 'waning_crescent_moon.png',
        ':waning_gibbous_moon:': 'waning_gibbous_moon.png',
        ':warning:': 'warning.png',
        ':watch:': 'watch.png',
        ':water_buffalo:': 'water_buffalo.png',
        ':watermelon:': 'watermelon.png',
        ':wave:': 'wave.png',
        ':wavy_dash:': 'wavy_dash.png',
        ':waxing_crescent_moon:': 'waxing_crescent_moon.png',
        ':waxing_gibbous_moon:': 'waxing_gibbous_moon.png',
        ':wc:': 'wc.png',
        ':weary:': 'weary.png',
        ':wedding:': 'wedding.png',
        ':whale2:': 'whale2.png',
        ':whale:': 'whale.png',
        ':wheelchair:': 'wheelchair.png',
        ':white_check_mark:': 'white_check_mark.png',
        ':white_circle:': 'white_circle.png',
        ':white_flower:': 'white_flower.png',
        ':white_large_square:': 'white_large_square.png',
        ':white_medium_small_square:': 'white_medium_small_square.png',
        ':white_medium_square:': 'white_medium_square.png',
        ':white_small_square:': 'white_small_square.png',
        ':white_square_button:': 'white_square_button.png',
        ':wind_chime:': 'wind_chime.png',
        ':wine_glass:': 'wine_glass.png',
        ':wink:': 'wink.png',
        ':wolf:': 'wolf.png',
        ':woman:': 'woman.png',
        ':womans_clothes:': 'womans_clothes.png',
        ':womans_hat:': 'womans_hat.png',
        ':womens:': 'womens.png',
        ':worried:': 'worried.png',
        ':wrench:': 'wrench.png',
        ':x:': 'x.png',
        ':yellow_heart:': 'yellow_heart.png',
        ':yen:': 'yen.png',
        ':yum:': 'yum.png',
        ':zap:': 'zap.png',
        ':zero:': 'zero.png',
        ':zzz:': 'zzz.png',

    }


def test(sender):
    print "%s initialized !!" % sender


def register():
    signals.content_object_init.connect(emojify)
    signals.article_writer_finalized.connect(save_emojis)


def mangle(generator):
    print "generator", generator


def emojify(content):
    if content is None:
        return
    if content._content is None:
        return
    if len(content._content) < 1:
        return
    for key in dict:
        if key in content._content:
            content._content = content._content.replace(key,
            '<img style="margin-bottom: -0.25em;height:1.5em;\
             display:inline-block;" src="/emojis/' + dict[key] + '">')
            used_emojis[key] = 1


def save_emojis(gen, writer):
    outpath = os.path.join(gen.output_path, "emojis")
    sourcepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
    "emojis")
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for key in used_emojis:
        shutil.copy(os.path.join(sourcepath, dict[key]),
        os.path.join(outpath, dict[key]))
