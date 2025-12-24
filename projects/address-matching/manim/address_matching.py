from manim import *

# --- CONFIGURATION ---
BI_ENCODER_COLOR = PURPLE_B
CROSS_ENCODER_COLOR = BLUE_D
DB_COLOR = GREY_D
EMBEDDING_COLOR = TEAL_C
BACKGROUND_COLOR = "#101010"

class AddressMatchingArchitecture(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        
        # --- TITLE ---
        title = Text("Siamese Transformer Address Matching", font_size=36).to_edge(UP)
        subtitle = Text("Bi-encoder + Cross-encoder Architecture", font_size=24, color=GREY).next_to(title, DOWN, buff=0.1)
        title_group = VGroup(title, subtitle)
        self.add(title_group)
        self.wait(1)

        # --- PHASE 1: PRE-EMBEDDING ---
        # 1. Normalized DB
        db_box = Rectangle(height=1.5, width=2.5, fill_color=DB_COLOR, fill_opacity=0.5, stroke_color=WHITE)
        db_label = Text("Normalized\nDatabase", font_size=20).move_to(db_box)
        db_group = VGroup(db_box, db_label).shift(LEFT * 4 + UP * 0.5)
        
        header_1 = Text("1. Database Pre-Embedding", font_size=24, color=BLUE).next_to(db_group, UP, buff=0.5).to_edge(LEFT, buff=1)
        example_addr = Text("Av. República, 1000-001", font_size=16, color=YELLOW).next_to(db_box, DOWN, buff=0.2)

        self.play(FadeIn(header_1), FadeIn(db_group), FadeIn(example_addr))

        # 2. Bi-Encoder
        bi_encoder = RoundedRectangle(corner_radius=0.2, height=1.2, width=2.2, fill_color=BI_ENCODER_COLOR, fill_opacity=0.8)
        bi_label = Text("Bi-Encoder", font_size=18).move_to(bi_encoder)
        bi_group = VGroup(bi_encoder, bi_label).next_to(db_group, RIGHT, buff=1.0)
        
        arrow_1 = Arrow(db_group.get_right(), bi_group.get_left(), buff=0.1)
        self.play(Create(bi_group), GrowArrow(arrow_1))

        # Animation of text passing through
        processing_text = example_addr.copy()
        self.play(processing_text.animate.move_to(bi_group.get_center()).scale(0.5).set_opacity(0), run_time=0.8)

        # 3. Embeddings (E_D)
        vector_box = Rectangle(height=1.2, width=1.5, color=WHITE)
        vector_lines = VGroup(*[Line(UP*0.4, DOWN*0.4, color=EMBEDDING_COLOR, stroke_width=4) for _ in range(4)]).arrange(RIGHT, buff=0.15)
        vector_lines.move_to(vector_box)
        vector_label = MathTex("E_D", font_size=24).next_to(vector_box, UP, buff=0.1)
        emb_group = VGroup(vector_box, vector_lines, vector_label).next_to(bi_group, RIGHT, buff=1.0)
        
        arrow_2 = Arrow(bi_group.get_right(), emb_group.get_left(), buff=0.1)
        self.play(GrowArrow(arrow_2), FadeIn(emb_group))

        # 4. Auxiliary DB (Grid)
        aux_box = Rectangle(height=1.8, width=1.8, color=GREY, stroke_width=2)
        aux_title = Text("9 Auxiliary Databases", font_size=14).next_to(aux_box, UP, buff=0.1)
        bins = VGroup()
        for i in range(1, 10):
            b = Square(side_length=0.35, fill_color=GREY_B, fill_opacity=0.5, stroke_width=1)
            t = Text(str(i), font_size=12, color=BLACK).move_to(b)
            bins.add(VGroup(b, t))
        bins.arrange_in_grid(rows=3, cols=3, buff=0.05).move_to(aux_box)
        aux_group = VGroup(aux_box, aux_title, bins).next_to(emb_group, RIGHT, buff=1.0)
        
        arrow_3 = Arrow(emb_group.get_right(), aux_group.get_left(), buff=0.1)
        self.play(GrowArrow(arrow_3), Create(aux_group))
        self.wait(1)

        # --- TRANSITION TO PHASE 2 ---
        # Explicit fade out to prevent text morphing glitches
        self.play(
            FadeOut(header_1), 
            FadeOut(title_group), FadeOut(example_addr), FadeOut(arrow_1), FadeOut(arrow_2), FadeOut(arrow_3),
            FadeOut(db_group), FadeOut(bi_group)
        )

        # Move E_D (Full DB) and Aux DB (Subsets) to "Shelf" positions (Top Left / Top Right)
        # This creates space in the center/bottom for the logic flow
        shelf_y = 2.5
        self.play(
            emb_group.animate.scale(0.7).move_to(np.array([-3, shelf_y, 0])),
            aux_group.animate.scale(0.7).move_to(np.array([3, shelf_y, 0]))
        )
        
        lbl_full = Text("Full DB", font_size=14).next_to(emb_group, UP, buff=0.1)
        lbl_aux = Text("Subsets", font_size=14).next_to(aux_group, UP, buff=0.1)
        self.play(FadeIn(lbl_full), FadeIn(lbl_aux))

        # --- PHASE 2: PREDICTING ---
        header_2 = Text("2. Predicting Module", font_size=24, color=BLUE).to_edge(LEFT).shift(UP * 0.5)
        self.play(FadeIn(header_2))

        # 1. Input (Bottom Left)
        input_box = Rectangle(height=1.2, width=2.5, fill_color=GREY_E, fill_opacity=1)
        input_label = Text("Un-Normalized\nAddress (x1)", font_size=16).move_to(input_box)
        # Shifted left and down to create a 'V' shape layout
        input_group = VGroup(input_box, input_label).to_edge(LEFT, buff=0.5).shift(DOWN * 2.0)
        
        messy_text = Text("av rep 10, 1000 lx", font_size=16, color=RED).next_to(input_box, UP, buff=0.1)
        self.play(FadeIn(input_group), FadeIn(messy_text))

        # 2. Bi-Encoder
        bi_encoder_2 = RoundedRectangle(corner_radius=0.2, height=1.0, width=2.0, fill_color=BI_ENCODER_COLOR, fill_opacity=0.8)
        bi_label_2 = Text("Bi-Encoder\n(Shared Weights)", font_size=14).move_to(bi_encoder_2)
        bi_group_2 = VGroup(bi_encoder_2, bi_label_2).next_to(input_group, RIGHT, buff=0.5)
        
        arrow_input = Arrow(input_group.get_right(), bi_group_2.get_left(), buff=0.1)
        self.play(Create(bi_group_2), GrowArrow(arrow_input))

        # 3. Embedding E1
        e1_vec = Line(UP*0.3, DOWN*0.3, color=RED, stroke_width=4)
        e1_label = MathTex("E_1", font_size=24).next_to(e1_vec, UP, buff=0.1)
        e1_group = VGroup(e1_vec, e1_label).next_to(bi_group_2, RIGHT, buff=0.5)
        self.play(FadeIn(e1_vec), FadeIn(e1_label))

        # 4. Decision Diamond (Center Bottom)
        decision_diamond = Polygon(UP, RIGHT, DOWN, LEFT, color=TEAL).scale(0.6).next_to(e1_group, RIGHT, buff=0.5)
        decision_text = Text("Has\nCP4?", font_size=12).move_to(decision_diamond)
        decision_group = VGroup(decision_diamond, decision_text)
        self.play(GrowArrow(Arrow(e1_group.get_right(), decision_group.get_left())), Create(decision_group))

        # 5. BRANCHING LOGIC (NO CROSSING)
        # Search Box placed Center-Right, between the shelves and the bottom row
        compare_box = Rectangle(height=1.0, width=2.0, color=BLUE)
        compare_text = Text("Cosine Sim\nSearch", font_size=16).move_to(compare_box)
        compare_group = VGroup(compare_box, compare_text).move_to(np.array([4, 0, 0]))

        # Path 1: YES (Yellow) -> Up to Aux DB
        path_yes = CurvedArrow(
            start_point=decision_diamond.get_top(),
            end_point=aux_group.get_left(),
            angle=-TAU/8, # Curve outward
            color=YELLOW, stroke_width=3
        )
        label_yes = Text("Yes", font_size=14, color=YELLOW).next_to(path_yes, LEFT, buff=-1).shift(UP*1.5)

        # Path 2: NO (Red) -> Up to Full DB
        path_no = CurvedArrow(
            start_point=decision_diamond.get_top(),
            end_point=emb_group.get_bottom(),
            angle=TAU/8, # Curve outward to left
            color=RED, stroke_width=3
        )
        label_no = Text("No", font_size=14, color=RED).next_to(path_no, LEFT, buff=0.1)

        # Show branches logic
        self.play(Create(path_yes), FadeIn(label_yes))
        self.play(Create(path_no), FadeIn(label_no))

        # CONVERGENCE: Both route to Search Box
        # Full DB -> Search
        return_no = DashedLine(emb_group.get_right(), compare_group.get_top() + LEFT*0.5, color=RED)
        # Aux DB -> Search
        return_yes = DashedLine(aux_group.get_bottom(), compare_group.get_top() + RIGHT*0.5, color=YELLOW)

        self.play(
            Create(return_no), 
            Create(return_yes), 
            FadeIn(compare_group)
        )

        # 6. Candidates (Top 10)
        candidates_box = Rectangle(height=1.5, width=1.5, fill_color=GREY_E, fill_opacity=1)
        c_text = Text("Top 10\nPairs", font_size=16).move_to(candidates_box)
        c_group = VGroup(candidates_box, c_text).next_to(compare_group, RIGHT, buff=0.5)
        
        self.play(GrowArrow(Arrow(compare_group.get_right(), c_group.get_left())), FadeIn(c_group))
        self.wait(1)

        # --- TRANSITION TO PHASE 3 (RE-RANKING) ---
        objects_to_fade = [
            header_2, input_group, messy_text, bi_group_2, arrow_input, 
            e1_group, decision_group, path_yes, label_yes, path_no, label_no,
            return_yes, return_no, compare_group, 
            emb_group, aux_group, lbl_full, lbl_aux, e1_vec, e1_label
        ]
        
        self.play(*[FadeOut(obj) for obj in objects_to_fade])
        
        # Smoothly move Top 10 to Left Edge for final stage
        self.play(c_group.animate.to_edge(LEFT, buff=2))

        # 7. Cross-Encoder
        ce_box = RoundedRectangle(corner_radius=0.2, height=2.0, width=4.0, fill_color=CROSS_ENCODER_COLOR, fill_opacity=0.8)
        ce_label = Text("Cross-Encoder\n(Re-Ranker)", font_size=24).move_to(ce_box).shift(UP*0.5)
        pair_viz = Text("[CLS] Input [SEP] Candidate", font_size=18, color=WHITE).move_to(ce_box).shift(DOWN*0.5)
        ce_group = VGroup(ce_box, ce_label, pair_viz).next_to(c_group, RIGHT, buff=1.5)

        self.play(Create(ce_group))

        # Particles
        for i in range(3):
            dot = Dot(color=YELLOW).move_to(c_group.get_right())
            self.play(dot.animate.move_to(ce_group.get_left()), run_time=0.3)
            self.play(Indicate(ce_box, color=WHITE), run_time=0.2)
            self.remove(dot)

        # 8. Final Result
        final_box = Rectangle(height=1.5, width=2.5, color=GREEN, stroke_width=4)
        final_text = Text("Door Acc:\n95.3%", font_size=24).move_to(final_box) 
        final_group = VGroup(final_box, final_text).next_to(ce_group, RIGHT, buff=1.0)

        self.play(GrowArrow(Arrow(ce_group.get_right(), final_group.get_left())), Write(final_group))
        self.wait(2)