print("=" * 50)
print("   THE CAVE OF SHADOWS")
print("=" * 50)
print()
print("You stand at the entrance of a dark cave.")
print("A cold wind blows from inside, carrying")
print("the faint sound of dripping water.")
print("Torchlight flickers on the stone walls.")
print()

choice1 = input("Do you (enter) the cave or (leave)? ")

if choice1 == "enter":
    print()
    print("You step inside. The air gets colder.")
    print("After a few steps, the tunnel splits in two.")
    print("The LEFT path glows faintly blue.")
    print("The RIGHT path smells like smoke.")
    print()

    choice2 = input("Go (left) or (right)? ")

    if choice2 == "left":
        print()
        print("You follow the blue glow and find an")
        print("underground lake. The water shimmers")
        print("with a strange light.")
        print("There's a small boat by the shore,")
        print("and something glittering at the bottom")
        print("of the lake.")
        print()

        choice3 = input("Take the (boat) or (dive) into the water? ")

        if choice3 == "boat":
            print()
            print("You row the boat to the center of the lake.")
            print("A treasure chest rises from the water!")
            print("Inside: a golden crown and ancient coins.")
            print()
            print("*** You found the treasure! You win! ***")
        elif choice3 == "dive":
            print()
            print("You dive into the glowing water.")
            print("It's warm! You swim deeper and find")
            print("an underwater tunnel that leads to")
            print("a hidden garden full of crystals.")
            print()
            print("*** You discovered the Crystal Garden! ***")
        else:
            print()
            print("You stand there, unsure. The glow fades.")
            print("You wander back out of the cave, empty-handed.")

    elif choice2 == "right":
        print()
        print("You follow the smoky path and find a")
        print("sleeping dragon curled around a pile of gold!")
        print("Its scales shimmer red and orange.")
        print()

        choice3 = input("Try to (sneak) past or (wake) the dragon? ")

        if choice3 == "sneak":
            print()
            print("You tiptoe past the dragon...")
            print("...and grab a handful of gold coins!")
            print("You make it out without waking it.")
            print()
            print("*** You escaped with dragon gold! ***")
        elif choice3 == "wake":
            print()
            print("The dragon opens one enormous eye.")
            print("'A visitor? How bold.'")
            print("It turns out this dragon loves riddles.")
            print("You spend the evening trading jokes")
            print("and it gives you a magic scale as a gift.")
            print()
            print("*** You befriended the dragon! ***")
        else:
            print()
            print("You freeze in fear. The dragon snores.")
            print("Eventually you back away slowly and leave.")

    else:
        print()
        print("You bump into a wall in the dark.")
        print("Ouch. You stumble back outside.")

elif choice1 == "leave":
    print()
    print("You decide the cave is too scary.")
    print("You walk back to town and buy a sandwich.")
    print("It's a really good sandwich, honestly.")
    print()
    print("*** The End (Sandwich Ending) ***")

else:
    print()
    print("You stand there, confused by your own choices.")
    print("A bat flies out of the cave and startles you.")
    print("You run away screaming.")
