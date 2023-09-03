import torch
import transformers
from langchain.llms import HuggingFacePipeline


def setup_llm(model_id="bigscience/bloom-560m"):
    device = (
        f"cuda:{torch.cuda.current_device()}" if torch.cuda.is_available() else "cpu"
    )

    print("Set up llm...")

    model_config = transformers.AutoConfig.from_pretrained(
        model_id,
    )

    model = transformers.AutoModelForCausalLM.from_pretrained(
        model_id,
        config=model_config,
        device_map=device,
    )

    tokenizer = transformers.AutoTokenizer.from_pretrained(
        model_id,
    )

    # enable evaluation mode to allow model inference
    model.eval()
    print(f"Model loaded on {device}")

    stop_list = ["\nHuman:", "\n```\n"]
    stop_token_ids = [tokenizer(x)["input_ids"] for x in stop_list]
    stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]

    # define custom stopping criteria object
    class StopOnTokens(transformers.StoppingCriteria):
        def __call__(
            self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
        ) -> bool:
            for stop_ids in stop_token_ids:
                if torch.eq(input_ids[0][-len(stop_ids) :], stop_ids).all():
                    return True
            return False

    stopping_criteria = transformers.StoppingCriteriaList([StopOnTokens()])

    generate_text = transformers.pipeline(
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,
        task="text-generation",
        # we pass model parameters here too
        stopping_criteria=stopping_criteria,
        temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
        max_new_tokens=64,  # max number of tokens to generate in the output
    )

    llm = HuggingFacePipeline(pipeline=generate_text)
    return llm
